#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);

function printHelp() {
  console.log(`Usage:
  node scripts/geo-deepseek-browser-direct.mjs --prompt <text> --out <file> [options]

Options:
  --session <id>      Session id recorded in output metadata.
  --prompt <text>     Prompt to send to DeepSeek.
  --timeout <sec>     Timeout passed to OpenCLI. Default: 300.
  --out <file>        Raw JSON output path.
  --profile <name>    OpenCLI Browser Bridge profile.
  --target <text>     Target entity recorded in output metadata.
  --no-search         Do not pass --search to DeepSeek.
  -h, --help          Show help.

Requires:
  npm install -g @jackwener/opencli
  opencli plugin install github:ssddi456/opencli-deepseek
`);
}

function parseArgs(argv) {
  const args = {
    session: '',
    prompt: '',
    timeout: 300,
    out: '',
    profile: '',
    target: '',
    search: true,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--session') args.session = takeValue(argv, ++i, arg);
    else if (arg === '--prompt') args.prompt = takeValue(argv, ++i, arg);
    else if (arg === '--timeout') args.timeout = Number(takeValue(argv, ++i, arg));
    else if (arg === '--out') args.out = takeValue(argv, ++i, arg);
    else if (arg === '--profile') args.profile = takeValue(argv, ++i, arg);
    else if (arg === '--target') args.target = takeValue(argv, ++i, arg);
    else if (arg === '--no-search') args.search = false;
    else if (arg === '-h' || arg === '--help') args.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  return args;
}

function takeValue(argv, index, option) {
  const value = argv[index];
  if (value == null || value === '' || value.startsWith('--')) {
    throw new Error(`${option} requires a value`);
  }
  return value;
}

function validate(args) {
  if (args.help) return;
  if (!args.prompt) throw new Error('Missing --prompt <text>');
  if (!args.out) throw new Error('Missing --out <file>');
  if (!Number.isInteger(args.timeout) || args.timeout < 30 || args.timeout > 1200) {
    throw new Error('--timeout must be an integer between 30 and 1200');
  }
}

function extractJson(text) {
  const raw = String(text || '').trim();
  const starts = [];
  for (let i = 0; i < raw.length; i += 1) {
    if (raw[i] === '[' || raw[i] === '{') starts.push(i);
  }
  for (const start of starts) {
    for (let end = raw.length; end > start; end -= 1) {
      const candidate = raw.slice(start, end).trim();
      if (!candidate) continue;
      try {
        return JSON.parse(candidate);
      } catch {
        // Try the next boundary.
      }
    }
  }
  return null;
}

function getResponse(parsed) {
  if (Array.isArray(parsed)) {
    const row = parsed.find((item) => item && typeof item === 'object') || {};
    return String(row.response || row.Response || row.answer || row.text || '').trim();
  }
  if (parsed && typeof parsed === 'object') {
    return String(parsed.response || parsed.Response || parsed.answer || parsed.text || '').trim();
  }
  return '';
}

function parseReferencesFromBrowserPayload(parsed) {
  if (!parsed || typeof parsed !== 'object') return [];
  const items = Array.isArray(parsed.references) ? parsed.references : [];
  return items.map((item) => normalizeReference(item)).filter(Boolean);
}

function normalizeReference(item) {
  if (!item || typeof item !== 'object') return null;
  const url = String(item.url || item.href || '').trim();
  if (!url) return null;
  const number = Number.parseInt(String(item.number || item.num || '').replace(/\D+/g, ''), 10) || null;
  const domain = item.domain || hostnameFromUrl(url);
  return {
    number,
    source: String(item.source || domain || '').trim(),
    domain: String(domain || '').trim(),
    title: String(item.title || titleFromUrl(url) || domain || url).trim(),
    date: String(item.date || '').trim(),
    url,
    summary: String(item.summary || item.context || '').trim(),
  };
}

function hostnameFromUrl(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return '';
  }
}

function titleFromUrl(url) {
  try {
    const parsed = new URL(url);
    const pathParts = parsed.pathname.split('/').filter(Boolean);
    const itemIndex = pathParts.findIndex((part) => part.toLowerCase() === 'item');
    if (itemIndex >= 0 && pathParts[itemIndex + 1]) {
      return decodeURIComponent(pathParts[itemIndex + 1]).replace(/[-_]+/g, ' ').slice(0, 120);
    }
    const tail = pathParts[pathParts.length - 1] || pathParts[pathParts.length - 2] || parsed.hostname;
    return decodeURIComponent(tail).replace(/[-_]+/g, ' ').slice(0, 120);
  } catch {
    return '';
  }
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(path.resolve(file)), { recursive: true });
  fs.writeFileSync(path.resolve(file), `${JSON.stringify(data, null, 2)}\n`);
}

async function runOpenCli(args) {
  const cliArgs = [];
  if (args.profile) cliArgs.push('--profile', args.profile);
  cliArgs.push(
    'deepseek',
    'ask',
    args.prompt,
    '--new',
    'true',
    '--timeout',
    String(args.timeout),
    '--format',
    'json',
    '--keep-tab',
    'true',
    '--site-session',
    'persistent',
    '--window',
    'foreground',
  );
  if (args.search) cliArgs.push('--search', 'true');

  const started = new Date();
  try {
    const result = await execFileAsync('opencli', cliArgs, {
      timeout: (args.timeout + 30) * 1000,
      maxBuffer: 30 * 1024 * 1024,
      env: process.env,
    });
    const output = `${result.stdout || ''}${result.stderr || ''}`;
    const parsed = extractJson(output);
    const answerText = getResponse(parsed);
    return {
      ok: Boolean(answerText),
      code: 0,
      output,
      parsed,
      answerText,
      started,
      finished: new Date(),
      error: answerText ? '' : 'OpenCLI returned no response text',
    };
  } catch (error) {
    const output = `${error.stdout || ''}${error.stderr || ''}`;
    const parsed = extractJson(output);
    const answerText = getResponse(parsed);
    return {
      ok: Boolean(answerText),
      code: error.code ?? 1,
      output,
      parsed,
      answerText,
      started,
      finished: new Date(),
      error: answerText ? '' : (output.trim() || error.message),
    };
  }
}

async function collectBrowserReferences(args) {
  if (!args.search) return { items: [], note: 'Search was disabled.' };
  const browserSession = args.session || 'yao-ds';
  const bindArgs = [];
  if (args.profile) bindArgs.push('--profile', args.profile);
  bindArgs.push('browser', browserSession, 'bind', '--window', 'foreground');
  try {
    await execFileAsync('opencli', bindArgs, {
      timeout: 15 * 1000,
      maxBuffer: 5 * 1024 * 1024,
      env: process.env,
    });
  } catch {
    // Continue: eval may still work if the session is already bound.
  }

  const js = `(() => {
    const messages = Array.from(document.querySelectorAll('.ds-message'));
    const candidates = messages.length ? messages : [document.body];
    const last = [...candidates].reverse().find((node) => {
      const text = (node.innerText || node.textContent || '').trim();
      return text.includes('已阅读') || node.querySelector('a[href^="http"]');
    }) || document.body;
    const anchors = Array.from(last.querySelectorAll('a[href^="http"]'));
    const seen = new Set();
    const references = [];
    for (const a of anchors) {
      const rawNum = (a.innerText || a.textContent || '').replace(/\\s+/g, '');
      const number = Number.parseInt(rawNum.replace(/\\D+/g, ''), 10) || null;
      const url = a.href || '';
      if (!url) continue;
      const key = (number || '') + '|' + url;
      if (seen.has(key)) continue;
      seen.add(key);
      let domain = '';
      try { domain = new URL(url).hostname.replace(/^www\\./, ''); } catch {}
      const contextNode = a.closest('tr,p,li,td,div') || a.parentElement;
      const context = (contextNode?.innerText || '').trim().slice(0, 500);
      references.push({
        number,
        url,
        domain,
        source: domain,
        title: a.title || a.getAttribute('aria-label') || '',
        summary: context
      });
    }
    const readMatch = (last.innerText || '').match(/已阅读\\s*(\\d+)\\s*个网页|^(\\d+)\\s*个网页$/m);
    return {
      href: location.href,
      title: document.title,
      read_count: readMatch ? Number(readMatch[1] || readMatch[2]) : null,
      references
    };
  })()`;
  const evalArgs = [];
  if (args.profile) evalArgs.push('--profile', args.profile);
  evalArgs.push('browser', browserSession, 'eval', js);
  try {
    const result = await execFileAsync('opencli', evalArgs, {
      timeout: 30 * 1000,
      maxBuffer: 20 * 1024 * 1024,
      env: process.env,
    });
    const parsed = extractJson(`${result.stdout || ''}${result.stderr || ''}`);
    const items = parseReferencesFromBrowserPayload(parsed);
    return {
      count_observed: parsed?.read_count || items.length,
      items,
      page_url: parsed?.href || '',
      page_title: parsed?.title || '',
      note: items.length
        ? 'References were extracted from the DeepSeek browser DOM citation links. DeepSeek did not expose a separate source-panel object through the public OpenCLI adapter.'
        : 'No citation links were found in the DeepSeek browser DOM.',
    };
  } catch (error) {
    return {
      items: [],
      note: `Browser reference extraction failed: ${error.message}`,
    };
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return;
  }
  validate(args);

  const run = await runOpenCli(args);
  const browserReferences = await collectBrowserReferences(args);
  const referenceItems = browserReferences.items || [];
  const raw = {
    schema_version: 'yao-deepseek-raw/opencli-plugin-v1',
    ok: run.ok,
    transport: 'opencli-deepseek-plugin',
    collected_at: run.finished.toISOString(),
    session: args.session,
    question: args.prompt,
    target: args.target,
    search: args.search,
    duration_ms: run.finished.getTime() - run.started.getTime(),
    answer: {
      text: run.answerText,
      length: run.answerText.length,
      target_mention_count: args.target ? countMentions(run.answerText, args.target) : 0,
    },
    references: {
      count: referenceItems.length,
      observed_count: browserReferences.count_observed || referenceItems.length,
      items: referenceItems,
      note: browserReferences.note,
      page_url: browserReferences.page_url || '',
      page_title: browserReferences.page_title || '',
    },
    opencli: {
      exit_code: run.code,
      parsed: run.parsed,
      output_excerpt: run.output.trim().slice(0, 4000),
    },
    error: run.error,
  };
  writeJson(args.out, raw);
  if (!run.ok) {
    console.error(run.error);
    process.exit(1);
  }
}

function countMentions(text, target) {
  const source = String(text || '');
  const needle = String(target || '').trim();
  if (!needle) return 0;
  return source.split(needle).length - 1;
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
