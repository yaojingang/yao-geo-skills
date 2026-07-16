#!/usr/bin/env node
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const crawlerScript = path.join(scriptDir, 'doubao_browser_crawl.mjs');
const batchScript = path.join(scriptDir, 'doubao_batch_crawl.mjs');
const analyzerScript = path.join(scriptDir, 'analyze_doubao_results.py');

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: options.cwd || path.dirname(scriptDir),
    encoding: 'utf8',
    env: options.env || process.env,
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return result;
}

function makeFakeOpenCli() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'fake-opencli-'));
  const executable = path.join(dir, 'opencli');
  fs.writeFileSync(executable, `#!/usr/bin/env node
const args = process.argv.slice(2);
const command = args[1];
const variant = process.env.FAKE_DOUBAO_CASE;
const prompt = command === 'ask' ? args[2] : '';
let rows;
if (command === 'ask' && variant === 'timeout') {
  rows = [
    { Role: 'User', Text: prompt },
    { Role: 'System', Text: 'No response within 300s. Doubao may still be generating.' },
  ];
} else if (command === 'read' && variant === 'timeout') {
  rows = [{ Role: 'System', Text: 'No visible Doubao messages were found.' }];
} else if (variant === 'captcha') {
  rows = [
    { Role: 'User', Text: prompt || '什么是 CAPTCHA？' },
    { Role: 'Assistant', Text: 'CAPTCHA 是一种区分人与机器的验证机制。' },
  ];
} else if (command === 'ask' && variant === 'page-chrome-1') {
  rows = [{ Role: 'Assistant', Text: '快速视频生成深入研究图像生成帮我写作音乐生成更多' }];
} else if (command === 'ask' && variant === 'page-chrome-2') {
  rows = [{ Role: 'Assistant', Text: 'AI创作云盘更多历史对话' }];
} else if (command === 'read' && variant.startsWith('page-chrome')) {
  rows = [{ Role: 'Assistant', Text: '好的。' }];
} else {
  rows = [{ Role: 'Assistant', Text: '正常回答' }];
}
process.stdout.write(JSON.stringify(rows));
`);
  fs.chmodSync(executable, 0o755);
  return dir;
}

function crawlWithFakeOpenCli(variant, prompt) {
  const fakeBin = makeFakeOpenCli();
  const result = run(process.execPath, [
    crawlerScript,
    '--prompt',
    prompt,
    '--no-new',
  ], {
    env: {
      ...process.env,
      FAKE_DOUBAO_CASE: variant,
      PATH: `${fakeBin}${path.delimiter}${process.env.PATH || ''}`,
    },
  });
  return JSON.parse(result.stdout);
}

test('timeout rows never turn the user prompt into a successful answer', () => {
  const record = crawlWithFakeOpenCli('timeout', '出国留学公司推荐');
  assert.equal(record.ok, false);
  assert.equal(record.answer.text, '');
});

test('assistant answers may discuss CAPTCHA without becoming failures', () => {
  const record = crawlWithFakeOpenCli('captcha', '什么是 CAPTCHA？');
  assert.equal(record.ok, true);
  assert.equal(record.answer.text, 'CAPTCHA 是一种区分人与机器的验证机制。');
});

test('readback replaces known Doubao assistant-area chrome', () => {
  const record = crawlWithFakeOpenCli('page-chrome-1', '测试问题');
  assert.equal(record.ok, true);
  assert.equal(record.answer.text, '好的。');
});

test('readback replaces known Doubao transcript chrome', () => {
  const record = crawlWithFakeOpenCli('page-chrome-2', '测试问题');
  assert.equal(record.ok, true);
  assert.equal(record.answer.text, '好的。');
});

test('batch output records when new conversations are disabled', () => {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'doubao-no-new-'));
  const questions = path.join(tempDir, 'questions.txt');
  const outDir = path.join(tempDir, 'run');
  fs.writeFileSync(questions, '测试问题\n');
  run(process.execPath, [
    batchScript,
    '--questions',
    questions,
    '--repeat',
    '1',
    '--dry-run',
    '--no-new',
    '--out-dir',
    outDir,
  ]);
  const dataset = JSON.parse(fs.readFileSync(path.join(outDir, 'doubao-crawl.json'), 'utf8'));
  assert.equal(dataset.input.new_conversation, false);
});

test('reports label web runs that reuse conversation context', () => {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'doubao-shared-context-'));
  const datasetPath = path.join(tempDir, 'doubao-crawl.json');
  const reportDir = path.join(tempDir, 'report');
  fs.writeFileSync(datasetPath, `${JSON.stringify({
    schema_version: 'yao-doubao-crawler/v1',
    run: {
      engine: 'doubao',
      transport: 'opencli-doubao-adapter',
    },
    input: {
      new_conversation: false,
      delay_strategy: { mode: 'fixed', delay_ms: 0 },
    },
    plan: [{
      sample_id: 'q01-r01',
      question_id: 'q01',
      question: '测试问题',
      repeat_index: 1,
    }],
    samples: [{
      sample_id: 'q01-r01',
      question_id: 'q01',
      question: '测试问题',
      repeat_index: 1,
      ok: true,
      result: {
        ok: true,
        question: '测试问题',
        answer: { text: '正常回答。' },
        references: { items: [] },
        transport: 'opencli-doubao-adapter',
      },
    }],
  }, null, 2)}\n`);
  run('python3', [analyzerScript, datasetPath, '--out-dir', reportDir]);
  const summary = JSON.parse(fs.readFileSync(path.join(reportDir, 'summary.json'), 'utf8'));
  const html = fs.readFileSync(path.join(reportDir, 'report.html'), 'utf8');
  assert.equal(summary.input.new_conversation, false);
  assert.match(html, /样本可能共享同一对话上下文/);
  assert.match(html, /Samples may share the same conversation context/);
});
