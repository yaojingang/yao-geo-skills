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
  if (action === 'bind') {
    if (process.env.FAKE_OPENCLI_CASE === 'bind-failure') {
      process.stderr.write('mock bind failed');
      process.exit(1);
    }
    process.exit(0);
  }
  if (action === 'unbind') {
    if (process.env.FAKE_OPENCLI_CASE === 'unbind-failure') {
      process.stderr.write('mock unbind failed');
      process.exit(1);
    }
    process.exit(0);
  }
  if (action === 'eval') {
    if (process.env.FAKE_OPENCLI_CASE === 'eval-failure') {
      process.stderr.write('mock eval failed');
      process.exit(1);
    }
    const wrongTab = process.env.FAKE_OPENCLI_CASE === 'wrong-tab';
    const wrongPrompt = process.env.FAKE_OPENCLI_CASE === 'wrong-prompt';
    const wrongAnswer = process.env.FAKE_OPENCLI_CASE === 'wrong-answer';
    const fingerprint = (value) => crypto.createHash('sha256').update(String(value).replace(/\\s+/g, ' ').trim(), 'utf8').digest('hex');
    process.stdout.write(JSON.stringify({
      href: wrongTab ? 'https://mail.example.test/inbox' : 'https://chat.deepseek.com/a/chat/s/11111111-1111-4111-8111-111111111111',
      title: wrongTab ? 'Inbox' : 'DeepSeek',
      prompt_matched: !wrongTab && !wrongPrompt,
      answer_matched: !wrongTab && !wrongPrompt && !wrongAnswer,
      matched_prompt: wrongTab ? '' : (wrongPrompt ? '旧提示词' : process.env.FAKE_EXPECTED_PROMPT),
      conversation_id: wrongTab ? '' : '11111111-1111-4111-8111-111111111111',
      answer_fingerprint: fingerprint(wrongAnswer ? 'Different answer' : 'Mock DeepSeek answer'),
      read_count: 1,
      references: [{
        number: 1,
        url: wrongTab || wrongPrompt || wrongAnswer ? 'https://private.example.test/message' : 'https://example.com/source',
        domain: wrongTab || wrongPrompt || wrongAnswer ? 'private.example.test' : 'example.com',
        source: wrongTab || wrongPrompt || wrongAnswer ? 'private.example.test' : 'example.com',
        title: wrongTab || wrongPrompt || wrongAnswer ? 'Private message' : 'Example source',
        summary: wrongTab || wrongPrompt || wrongAnswer ? 'Private context' : 'Answer citation context'
      }]
    }));
    process.exit(0);
  }
}

if (args.includes('deepseek') && args.includes('ask')) {
  process.stdout.write(JSON.stringify({ response: 'Mock DeepSeek answer' }));
  process.exit(0);
}

process.stderr.write('unexpected fake opencli command: ' + args.join(' '));
process.exit(2);
`);
  fs.chmodSync(executable, 0o755);
  return executable;
}

function runCrawler(variant) {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'deepseek-crawler-test-'));
  tempDirs.push(tempDir);
  const outputPath = path.join(tempDir, 'raw.json');
  const logPath = path.join(tempDir, 'opencli.log');
  const prompt = '新能源汽车推荐';
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
  assert.deepEqual(commands.map(browserAction), ['ask', 'bind', 'eval', 'unbind']);
});

test('rejects evidence from a DeepSeek page whose latest prompt does not match', () => {
  const { commands, record } = runCrawler('wrong-prompt');
  assert.equal(record.ok, true);
  assert.equal(record.references.count, 0);
  assert.equal(record.references.verified, false);
  assert.match(record.references.note, /rejected/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'bind', 'eval', 'unbind']);
});

test('rejects evidence from a repeated prompt whose assistant answer does not match', () => {
  const { commands, record } = runCrawler('wrong-answer');
  assert.equal(record.ok, true);
  assert.equal(record.references.count, 0);
  assert.equal(record.references.verified, false);
  assert.match(record.references.note, /rejected/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'bind', 'eval', 'unbind']);
});

test('keeps verified DeepSeek citations and unbinds after successful extraction', () => {
  const { commands, record } = runCrawler('success');
  assert.equal(record.references.count, 1);
  assert.equal(record.references.verified, true);
  assert.equal(record.references.answer_matched, true);
  assert.equal(record.references.conversation_id, '11111111-1111-4111-8111-111111111111');
  const answerFingerprint = createHash('sha256').update('Mock DeepSeek answer', 'utf8').digest('hex');
  assert.equal(record.references.answer_fingerprint, answerFingerprint);
  assert.deepEqual(commands.map(browserAction), ['ask', 'bind', 'eval', 'unbind']);

  const evalCommand = commands.find((command) => browserAction(command) === 'eval');
  const evalScript = evalCommand.at(-1);
  assert.match(evalScript, /chat\.deepseek\.com/);
  assert.match(evalScript, /新能源汽车推荐/);
  assert.match(evalScript, new RegExp(answerFingerprint));
  assert.doesNotMatch(evalScript, /Mock DeepSeek answer/);
  assert.doesNotMatch(evalScript, /\[document\.body\]|\|\|\s*document\.body/);
});

test('unbinds after browser evaluation fails', () => {
  const { commands, record } = runCrawler('eval-failure');
  assert.equal(record.references.count, 0);
  assert.equal(record.references.verified, false);
  assert.match(record.references.note, /failed/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'bind', 'eval', 'unbind']);
});

test('unbinds after browser session binding fails', () => {
  const { commands, record } = runCrawler('bind-failure');
  assert.equal(record.references.count, 0);
  assert.equal(record.references.verified, false);
  assert.match(record.references.note, /bind failed/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'bind', 'unbind']);
});

test('records an unbind failure without discarding verified citations', () => {
  const { commands, record } = runCrawler('unbind-failure');
  assert.equal(record.references.count, 1);
  assert.equal(record.references.verified, true);
  assert.match(record.references.cleanup_error, /unbind failed/i);
  assert.match(record.references.note, /unbind failed/i);
  assert.deepEqual(commands.map(browserAction), ['ask', 'bind', 'eval', 'unbind']);
});
