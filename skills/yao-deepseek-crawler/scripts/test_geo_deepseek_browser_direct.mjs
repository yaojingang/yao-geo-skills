#!/usr/bin/env node
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test, { after } from 'node:test';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const crawlerScript = path.join(scriptDir, 'geo-deepseek-browser-direct.mjs');
const tempDirs = [];

after(() => {
  for (const tempDir of tempDirs) {
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
});

function makeFakeOpenCli(tempDir) {
  const executable = path.join(tempDir, 'opencli');
  fs.writeFileSync(executable, `#!/usr/bin/env node
const fs = require('node:fs');
const crypto = require('node:crypto');
const args = process.argv.slice(2);
fs.appendFileSync(process.env.FAKE_OPENCLI_LOG, JSON.stringify(args) + '\\n');

const browserIndex = args.indexOf('browser');
if (browserIndex >= 0) {
  const action = args[browserIndex + 2];
  if (action === 'open') {
    if (process.env.FAKE_OPENCLI_CASE === 'open-failure') {
      process.stderr.write('mock open failed');
      process.exit(1);
    }
    process.stdout.write(JSON.stringify({ url: args[browserIndex + 3], page: 'owned-tab-1' }));
    process.exit(0);
  }
  if (action === 'close') {
    if (process.env.FAKE_OPENCLI_CASE === 'close-failure') {
      process.stderr.write('mock close failed');
      process.exit(1);
    }
    process.exit(0);
  }
  if (action === 'wait') {
    process.stdout.write(JSON.stringify({ matched: true, type: 'selector', value: '.ds-message' }));
    process.exit(0);
  }
  if (action === 'eval') {
    const evalScript = args.at(-1);
    const isExtraction = evalScript.includes('const expectedPrompt =');
    if (!isExtraction) {
      process.stdout.write('https://chat.deepseek.com/a/chat/s/11111111-1111-4111-8111-111111111111');
      process.exit(0);
    }
    if (process.env.FAKE_OPENCLI_CASE === 'eval-failure') {
      process.stderr.write('mock eval failed');
      process.exit(1);
    }
    const wrongTab = process.env.FAKE_OPENCLI_CASE === 'wrong-tab';
    const wrongPrompt = process.env.FAKE_OPENCLI_CASE === 'wrong-prompt';
    const wrongAnswer = process.env.FAKE_OPENCLI_CASE === 'wrong-answer';
    const href = wrongTab
      ? 'https://mail.example.test/inbox'
      : 'https://chat.deepseek.com/a/chat/s/11111111-1111-4111-8111-111111111111';
    const parsedHref = new URL(href);
    const location = { href, origin: parsedHref.origin, pathname: parsedHref.pathname };
    const promptText = wrongPrompt ? '旧提示词' : process.env.FAKE_EXPECTED_PROMPT;
    const answerText = wrongAnswer ? 'Different answer' : (process.env.FAKE_DOM_ANSWER || 'Mock DeepSeek answer');
    const contextNode = { innerText: 'Answer citation context' };
    const anchor = {
      innerText: '1',
      textContent: '1',
      href: 'https://example.com/source',
      title: 'Example source',
      getAttribute(name) { return name === 'aria-label' ? 'Example source' : ''; },
      closest() { return contextNode; },
      parentElement: contextNode,
    };
    const markdown = { innerText: answerText, textContent: answerText };
    const makeMessage = (role, text) => ({
      getAttribute(name) { return name === 'data-role' ? role : ''; },
      classList: { length: 1 },
      innerText: role === 'assistant' ? '已阅读 1 个网页\\n' + text + '\\n1 个网页' : text,
      textContent: role === 'assistant' ? '已阅读 1 个网页 ' + text + ' 1 个网页' : text,
      querySelector(selector) {
        return role === 'assistant' && selector.includes('.ds-markdown') ? markdown : null;
      },
      querySelectorAll(selector) {
        return role === 'assistant' && selector === 'a[href^="http"]' ? [anchor] : [];
      },
    });
    const messages = [makeMessage('user', promptText), makeMessage('assistant', answerText)];
    const document = {
      title: wrongTab ? 'Inbox' : 'DeepSeek',
      querySelectorAll(selector) { return selector === '.ds-message' ? messages : []; },
      querySelector() { return null; },
    };
    Promise.resolve(eval(evalScript)).then((payload) => {
      process.stdout.write(JSON.stringify(payload));
    }).catch((error) => {
      process.stderr.write(error.stack || error.message);
      process.exitCode = 1;
    });
    return;
  }
}

if (args.includes('deepseek') && args.includes('ask')) {
  process.stdout.write(JSON.stringify({ response: process.env.FAKE_RESPONSE || 'Mock DeepSeek answer' }));
  process.exit(0);
}

process.stderr.write('unexpected fake opencli command: ' + args.join(' '));
process.exit(2);
`);
  fs.chmodSync(executable, 0o755);
  return executable;
}

function runCrawler(variant, options = {}) {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'deepseek-crawler-test-'));
  tempDirs.push(tempDir);
  const outputPath = path.join(tempDir, 'raw.json');
  const logPath = path.join(tempDir, 'opencli.log');
  const prompt = options.prompt || '新能源汽车推荐';
  makeFakeOpenCli(tempDir);
  const result = spawnSync(process.execPath, [
    crawlerScript,
    '--session',
    'test-session',
    '--prompt',
    prompt,
    '--out',
    outputPath,
  ], {
    cwd: path.dirname(scriptDir),
    encoding: 'utf8',
    env: {
      ...process.env,
      FAKE_EXPECTED_PROMPT: prompt,
      FAKE_RESPONSE: options.response || 'Mock DeepSeek answer',
      FAKE_DOM_ANSWER: options.domAnswer || 'Mock DeepSeek answer',
      FAKE_OPENCLI_CASE: variant,
      FAKE_OPENCLI_LOG: logPath,
      PATH: `${tempDir}${path.delimiter}${process.env.PATH || ''}`,
    },
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const record = JSON.parse(fs.readFileSync(outputPath, 'utf8'));
  const commands = fs.readFileSync(logPath, 'utf8')
    .trim()
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
  return { commands, record };
}

function browserAction(command) {
  const browserIndex = command.indexOf('browser');
  return browserIndex >= 0 ? command[browserIndex + 2] : 'ask';
}

test('rejects evidence from a foreground tab outside the submitted DeepSeek prompt', () => {
  const { commands, record } = runCrawler('wrong-tab');
  assert.equal(record.ok, true);
  assert.equal(record.references.count, 0);
  assert.equal(record.references.verified, false);
  assert.match(record.references.note, /rejected/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'open', 'eval', 'open', 'wait', 'eval', 'close']);
});

test('rejects evidence from a DeepSeek page whose latest prompt does not match', () => {
  const { commands, record } = runCrawler('wrong-prompt');
  assert.equal(record.ok, true);
  assert.equal(record.references.count, 0);
  assert.equal(record.references.verified, false);
  assert.match(record.references.note, /rejected/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'open', 'eval', 'open', 'wait', 'eval', 'close']);
});

test('rejects evidence from a repeated prompt whose assistant answer does not match', () => {
  const { commands, record } = runCrawler('wrong-answer');
  assert.equal(record.ok, true);
  assert.equal(record.references.count, 0);
  assert.equal(record.references.verified, false);
  assert.match(record.references.note, /rejected/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'open', 'eval', 'open', 'wait', 'eval', 'close']);
});

test('keeps verified DeepSeek citations in an owned browser session', () => {
  const { commands, record } = runCrawler('success');
  assert.equal(record.references.count, 1);
  assert.equal(record.references.verified, true);
  assert.equal(record.references.answer_matched, true);
  assert.equal(record.references.conversation_id, '11111111-1111-4111-8111-111111111111');
  const answerFingerprint = createHash('sha256').update('Mock DeepSeek answer', 'utf8').digest('hex');
  assert.equal(record.references.answer_fingerprint, answerFingerprint);
  assert.deepEqual(commands.map(browserAction), ['ask', 'open', 'eval', 'open', 'wait', 'eval', 'close']);

  const evalCommand = commands.find((command) => (
    browserAction(command) === 'eval' && command.at(-1).includes('const expectedPrompt =')
  ));
  const evalScript = evalCommand.at(-1);
  assert.match(evalScript, /chat\.deepseek\.com/);
  assert.match(evalScript, /新能源汽车推荐/);
  assert.match(evalScript, new RegExp(answerFingerprint));
  assert.doesNotMatch(evalScript, /Mock DeepSeek answer/);
  assert.doesNotMatch(evalScript, /\[document\.body\]|\|\|\s*document\.body/);
});

test('keeps a submitted prompt whose text ends with a web-page count', () => {
  const { record } = runCrawler('success', { prompt: '请总结以下 10 个网页' });
  assert.equal(record.references.count, 1);
  assert.equal(record.references.verified, true);
});

test('matches an answer after removing DeepSeek search-status text', () => {
  const { record } = runCrawler('success', {
    response: '已阅读 1 个网页\nMock DeepSeek answer\n1 个网页',
    domAnswer: 'Mock DeepSeek answer',
  });
  const answerFingerprint = createHash('sha256').update('Mock DeepSeek answer', 'utf8').digest('hex');
  assert.equal(record.references.answer_fingerprint, answerFingerprint);
  assert.equal(record.references.verified, true);
});

test('closes the owned browser session after evaluation fails', () => {
  const { commands, record } = runCrawler('eval-failure');
  assert.equal(record.references.count, 0);
  assert.equal(record.references.verified, false);
  assert.match(record.references.note, /failed/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'open', 'eval', 'open', 'wait', 'eval', 'close']);
});

test('closes the owned browser session after opening it fails', () => {
  const { commands, record } = runCrawler('open-failure');
  assert.equal(record.references.count, 0);
  assert.equal(record.references.verified, false);
  assert.match(record.references.note, /navigation failed/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'open', 'close']);
});

test('records a close failure without discarding verified citations', () => {
  const { commands, record } = runCrawler('close-failure');
  assert.equal(record.references.count, 1);
  assert.equal(record.references.verified, true);
  assert.match(record.references.cleanup_error, /close failed/i);
  assert.match(record.references.note, /close failed/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'open', 'eval', 'open', 'wait', 'eval', 'close']);
});
