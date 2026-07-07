#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

function parseArgs(argv) {
  const args = {
    timeout: 300,
    referenceExtraction: true,
    profile: '',
    siteSession: 'persistent',
    newConversation: true,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--prompt' || arg === '-p') args.prompt = argv[++i];
    else if (arg === '--profile') args.profile = argv[++i];
    else if (arg === '--timeout') args.timeout = Number(argv[++i]);
    else if (arg === '--out') args.out = argv[++i];
    else if (arg === '--target' || arg === '--target-entity') args.target = argv[++i];
    else if (arg === '--site-session') args.siteSession = argv[++i];
    else if (arg === '--no-search' || arg === '--no-reference-extraction') args.referenceExtraction = false;
    else if (arg === '--no-new') args.newConversation = false;
    else if (arg === '--capture-current') args.captureCurrent = true;
    else if (arg === '-h' || arg === '--help') args.help = true;
    else if (!args.prompt) args.prompt = arg;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node scripts/doubao_browser_crawl.mjs --profile <profile> --prompt <question> [options]

Options:
  --profile <name>        OpenCLI Browser Bridge profile alias/id.
  --timeout <seconds>     Max seconds to wait. Default: 300.
  --target <text>         Optional target term to count in the answer.
  --target-entity <text>  Alias for --target.
  --site-session <mode>   OpenCLI site session: persistent or ephemeral. Default: persistent.
  --no-reference-extraction
                           Skip visible URL extraction from the answer text.
  --no-search             Alias for --no-reference-extraction, kept for batch compatibility.
  --no-new                Do not call opencli doubao new before asking.
  --capture-current       Capture the current Doubao conversation instead of sending.
  --out <file>            Save normalized JSON.
  -h, --help              Show help.
`);
}

function validateOptions(options) {
  if (options.help) return;
  if (!options.captureCurrent && !options.prompt) throw new Error('Missing --prompt <question>');
  if (!Number.isInteger(options.timeout) || options.timeout < 30 || options.timeout > 7200) {
    throw new Error('--timeout must be an integer between 30 and 7200');
  }
  if (!['persistent', 'ephemeral'].includes(options.siteSession)) {
    throw new Error('--site-session must be persistent or ephemeral');
  }
}

function runOpenCli(args, options = {}) {
  const fullArgs = [];
  if (options.profile) fullArgs.push('--profile', options.profile);
  fullArgs.push(...args);
  try {
    return execFileSync('opencli', fullArgs, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: options.timeoutMs ?? 360000,
      maxBuffer: 20 * 1024 * 1024,
    });
  } catch (error) {
    const output = `${error.stdout ?? ''}${error.stderr ?? ''}`.trim();
    throw new Error(output || error.message);
  }
}

function parseJsonFromOpenCli(output) {
  const trimmed = String(output || '').trim();
  try {
    return JSON.parse(trimmed);
  } catch {}
  const arrayStart = trimmed.indexOf('[');
  const objectStart = trimmed.indexOf('{');
  const starts = [arrayStart, objectStart].filter((index) => index >= 0);
  if (!starts.length) throw new Error(`No JSON found in opencli output:\n${trimmed}`);
  const start = Math.min(...starts);
  const lastArray = trimmed.lastIndexOf(']');
  const lastObject = trimmed.lastIndexOf('}');
  const end = Math.max(lastArray, lastObject);
  if (end < start) throw new Error(`Malformed JSON in opencli output:\n${trimmed}`);
  return JSON.parse(trimmed.slice(start, end + 1));
}

function cleanText(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function multilineText(value) {
  return String(value || '').replace(/\r\n/g, '\n').trim();
}

function compactOutput(value, maxLength = 5000) {
  const text = multilineText(value);
  return text.length <= maxLength ? text : `${text.slice(0, maxLength)}...`;
}

function firstRecord(value) {
  if (Array.isArray(value)) return firstRecord(value[0]);
  if (!value || typeof value !== 'object') return value;
  for (const key of ['data', 'rows', 'result', 'results']) {
    if (Array.isArray(value[key]) && value[key].length) return firstRecord(value[key][0]);
    if (value[key] && typeof value[key] === 'object') return firstRecord(value[key]);
  }
  return value;
}

function findStringByKeys(value, keys) {
  if (!value) return '';
  if (typeof value === 'string') return '';
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = findStringByKeys(item, keys);
      if (found) return found;
    }
    return '';
  }
  if (typeof value !== 'object') return '';
  for (const key of keys) {
    if (typeof value[key] === 'string' && cleanText(value[key])) return multilineText(value[key]);
  }
  for (const child of Object.values(value)) {
    const found = findStringByKeys(child, keys);
    if (found) return found;
  }
  return '';
}

function directText(value) {
  if (!value || typeof value !== 'object') return '';
  for (const key of ['response', 'answer', 'assistant', 'content', 'Text', 'text']) {
    if (typeof value[key] === 'string' && cleanText(value[key])) return multilineText(value[key]);
  }
  return '';
}

function extractAssistantMessage(value) {
  if (!value) return '';
  if (Array.isArray(value)) {
    for (let i = value.length - 1; i >= 0; i -= 1) {
      const found = extractAssistantMessage(value[i]);
      if (found) return found;
    }
    return '';
  }
  if (typeof value !== 'object') return '';
  const role = cleanText(value.role || value.Role || value.author || value.Author).toLowerCase();
  const userRole = /user|human|用户|我|访客/.test(role);
  const assistantRole = /assistant|bot|doubao|豆包|ai|智能体/.test(role);
  const systemRole = /system|系统|tool|工具/.test(role);
  if (assistantRole && !userRole && !systemRole) {
    const text = directText(value);
    if (text) return text;
  }
  for (const key of ['messages', 'rows', 'data', 'result', 'results']) {
    if (value[key]) {
      const found = extractAssistantMessage(value[key]);
      if (found) return found;
    }
  }
  return '';
}

function extractAnswerText(parsed) {
  const assistantMessage = extractAssistantMessage(parsed);
  if (assistantMessage) return assistantMessage;
  const record = firstRecord(parsed);
  const direct = findStringByKeys(record, ['response', 'answer', 'assistant', 'content', 'Text', 'text']);
  if (direct) return direct;
  if (typeof record === 'string') return multilineText(record);
  return '';
}

function extractConversation(parsed) {
  const record = firstRecord(parsed);
  return {
    id: findStringByKeys(record, ['conversationId', 'conversation_id', 'id']),
    url: findStringByKeys(record, ['conversationUrl', 'conversation_url', 'url']),
    tool: findStringByKeys(record, ['tool']),
  };
}

function extractHeadings(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => /^#{1,6}\s+\S/.test(line))
    .map((line) => line.replace(/^#{1,6}\s+/, ''));
}

function countOccurrences(text, target) {
  if (!target) return null;
  const escaped = target.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const matches = text.match(new RegExp(escaped, 'gi'));
  return matches ? matches.length : 0;
}

function domainFromUrl(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, '').toLowerCase();
  } catch {
    return '';
  }
}

function stripTrailingPunctuation(url) {
  return String(url || '').replace(/[),\].。；;，、,.]+$/g, '');
}

function collectReferencesFromText(text) {
  const items = [];
  const seen = new Set();
  const excludedDomains = new Set(['doubao.com']);

  const add = (title, url) => {
    const cleanedUrl = stripTrailingPunctuation(url);
    const domain = domainFromUrl(cleanedUrl);
    if (!cleanedUrl || !domain || excludedDomains.has(domain)) return;
    const key = cleanedUrl.toLowerCase();
    if (seen.has(key)) return;
    seen.add(key);
    items.push({
      number: items.length + 1,
      source: domain,
      domain,
      title: cleanText(title) || domain,
      date: '',
      url: cleanedUrl,
      summary: '',
    });
  };

  const markdownLink = /\[([^\]\n]{1,220})\]\((https?:\/\/[^)\s]+)\)/g;
  for (const match of text.matchAll(markdownLink)) add(match[1], match[2]);

  const bareUrl = /https?:\/\/[^\s<>"')\]]+/g;
  for (const match of text.matchAll(bareUrl)) add('', match[0]);

  return {
    requested: true,
    count: items.length,
    items,
    note: items.length ? '' : 'No external URLs were found in the Doubao answer text.',
  };
}

function captureCurrent(options) {
  const readArgs = [
    'doubao',
    'read',
    '-f',
    'json',
    '--site-session',
    options.siteSession,
    '--keep-tab',
    'false',
  ];
  const output = runOpenCli(readArgs, {
    profile: options.profile,
    timeoutMs: options.timeout * 1000,
  });
  const parsed = parseJsonFromOpenCli(output);
  return { parsed, output };
}

function readCurrentConversation(options) {
  const readArgs = [
    'doubao',
    'read',
    '-f',
    'json',
    '--site-session',
    options.siteSession,
    '--keep-tab',
    'true',
    '--window',
    'foreground',
  ];
  const output = runOpenCli(readArgs, {
    profile: options.profile,
    timeoutMs: options.timeout * 1000,
  });
  const parsed = parseJsonFromOpenCli(output);
  return { parsed, output };
}

function startNewConversation(options) {
  if (!options.newConversation) return null;
  const newArgs = [
    'doubao',
    'new',
    '-f',
    'json',
    '--site-session',
    options.siteSession,
    '--keep-tab',
    'true',
    '--window',
    'foreground',
  ];
  const output = runOpenCli(newArgs, {
    profile: options.profile,
    timeoutMs: 120000,
  });
  return {
    parsed: parseJsonFromOpenCli(output),
    output,
  };
}

function askDoubao(options) {
  const newConversationState = startNewConversation(options);
  const askArgs = [
    'doubao',
    'ask',
    options.prompt,
    '--timeout',
    String(options.timeout),
    '-f',
    'json',
    '--site-session',
    options.siteSession,
    '--keep-tab',
    'true',
    '--window',
    'foreground',
  ];

  const output = runOpenCli(askArgs, {
    profile: options.profile,
    timeoutMs: (options.timeout + 45) * 1000,
  });
  const parsed = parseJsonFromOpenCli(output);
  return { parsed, output, newConversationState };
}

function looksLikePageChrome(text) {
  const source = cleanText(text);
  if (!source) return true;
  const uiMarkers = ['新办公任务', '历史对话', '快速帮我写作', '编程PPT', 'AI 创作', '云盘更多'];
  const markerCount = uiMarkers.filter((marker) => source.includes(marker)).length;
  return markerCount >= 3 && !/[。！？]\s*/.test(source.slice(0, 120));
}

function looksLikeFailureText(text) {
  const source = cleanText(text).toLowerCase();
  if (!source) return true;
  return [
    'no response within',
    'no visible doubao messages',
    'auth_required',
    'region-ban',
    'captcha',
  ].some((marker) => source.includes(marker));
}

function chooseAnswerText(primaryText, fallbackText, target = '') {
  const primary = multilineText(primaryText);
  const fallback = multilineText(fallbackText);
  if (looksLikeFailureText(primary) && !looksLikeFailureText(fallback)) return fallback;
  if (looksLikeFailureText(fallback)) return primary;
  if (!fallback) return primary;
  if (!primary) return fallback;
  if (looksLikePageChrome(primary) && !looksLikePageChrome(fallback)) return fallback;
  if (target && !primary.includes(target) && fallback.includes(target)) return fallback;
  if (fallback.length > primary.length * 1.4 && !looksLikePageChrome(fallback)) return fallback;
  return primary;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }
  validateOptions(options);

  const startedAt = new Date().toISOString();
  const raw = options.captureCurrent ? captureCurrent(options) : askDoubao(options);
  let readBack = null;
  if (!options.captureCurrent) {
    try {
      readBack = readCurrentConversation(options);
    } catch {
      readBack = null;
    }
  }
  const askAnswerText = extractAnswerText(raw.parsed);
  const readAnswerText = readBack ? extractAnswerText(readBack.parsed) : '';
  const answerText = chooseAnswerText(askAnswerText, readAnswerText, options.target);
  const conversation = extractConversation(readBack?.parsed || raw.parsed);
  const references = options.referenceExtraction
    ? collectReferencesFromText(answerText)
    : { requested: false, count: 0, items: [], note: 'Reference extraction was not requested.' };

  const record = {
    ok: Boolean(cleanText(answerText)) && !looksLikeFailureText(answerText),
    collected_at: new Date().toISOString(),
    engine: 'doubao',
    transport: 'opencli-doubao-adapter',
    question: options.prompt || '',
    options: {
      profile: options.profile || null,
      site_session: options.siteSession,
      reference_extraction: options.referenceExtraction,
      new_conversation: Boolean(options.newConversation && !options.captureCurrent),
      capture_current: Boolean(options.captureCurrent),
      started_at: startedAt,
    },
    page: {
      url: conversation.url || null,
      title: 'Doubao',
      conversation_id: conversation.id || null,
    },
    answer: {
      text: answerText,
    },
    references,
    extraction: {
      char_count: answerText.length,
      line_count: answerText ? answerText.split(/\r?\n/).length : 0,
      headings: extractHeadings(answerText),
      reference_count: references.count,
      target: options.target ?? null,
      target_mention_count: countOccurrences(answerText, options.target),
    },
    raw: {
      opencli_result: raw.parsed,
      opencli_output_excerpt: compactOutput(raw.output),
      opencli_readback_result: readBack?.parsed || null,
      opencli_readback_output_excerpt: readBack ? compactOutput(readBack.output) : '',
      new_conversation_state: raw.newConversationState || null,
      tool: conversation.tool || null,
    },
  };

  if (options.out) {
    fs.mkdirSync(path.dirname(path.resolve(options.out)), { recursive: true });
    fs.writeFileSync(path.resolve(options.out), `${JSON.stringify(record, null, 2)}\n`);
  }
  console.log(JSON.stringify(record, null, 2));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
