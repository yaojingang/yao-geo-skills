#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const scriptDir = path.dirname(__filename);
const skillRoot = path.resolve(scriptDir, '..');
const defaultCrawlerScript = path.join(scriptDir, 'geo-deepseek-browser-direct.mjs');
const MINUTE_MS = 60 * 1000;
const MAX_DELAY_MS = 24 * 60 * 60 * 1000;

function printHelp() {
  console.log(`Usage:
  node scripts/deepseek_batch_crawl.mjs --questions <file> --repeat <n> [options]

Options:
  --questions <file>        Text file, JSON array of strings, or JSON array of objects.
  --repeat <n>              Global repeat count per question. Default: 5.
  --profile <name>          OpenCLI Browser Bridge profile.
  --target <text>           Optional target term passed to the underlying crawler.
  --target-entity <text>    Required for standard reports. Primary entity to diagnose.
  --target-aliases <text>   Optional aliases separated by comma, pipe, semicolon, or newline.
  --entity-type <type>      Required with --target-entity: person/company/product or 人/公司/产品.
  --out-dir <dir>           Run output directory. Default: runs/<timestamp>.
  --crawler-script <file>   Existing DeepSeek crawler script. Defaults to scripts/geo-deepseek-browser-direct.mjs.
  --timeout <seconds>       Per-sample timeout passed to crawler. Default: 300.
  --delay-ms <ms>           Delay between samples. Default: 1500.
  --safe-random-delay       Random delay of 5-20 minutes between fresh samples.
  --delay-min-minutes <n>   Custom random delay lower bound, in minutes.
  --delay-max-minutes <n>   Custom random delay upper bound, in minutes.
  --delay-min-ms <ms>       Custom random delay lower bound, in milliseconds.
  --delay-max-ms <ms>       Custom random delay upper bound, in milliseconds.
  --resume                  Reuse existing raw JSON files when valid.
  --dry-run                 Write the plan without running DeepSeek.
  --no-search               Pass --no-search to the underlying crawler.
  -h, --help                Show help.
`);
}

function parseArgs(argv) {
  const args = {
    repeat: 5,
    timeout: 300,
    delayMs: 1500,
    search: true,
    resume: false,
    dryRun: false,
    profile: '',
    target: '',
    targetEntity: '',
    targetAliases: [],
    entityType: '',
    delayMinMs: null,
    delayMaxMs: null,
    crawlerScript: process.env.DEEPSEEK_CRAWLER_SCRIPT || defaultCrawlerScript,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--questions') args.questions = takeArgValue(argv, ++i, arg);
    else if (arg === '--repeat') args.repeat = Number(takeArgValue(argv, ++i, arg));
    else if (arg === '--profile') args.profile = takeArgValue(argv, ++i, arg);
    else if (arg === '--target') args.target = takeArgValue(argv, ++i, arg);
    else if (arg === '--target-entity') args.targetEntity = takeArgValue(argv, ++i, arg);
    else if (arg === '--target-aliases') args.targetAliases = splitAliases(takeArgValue(argv, ++i, arg));
    else if (arg === '--entity-type') args.entityType = normalizeEntityType(takeArgValue(argv, ++i, arg));
    else if (arg === '--out-dir') args.outDir = takeArgValue(argv, ++i, arg);
    else if (arg === '--crawler-script') args.crawlerScript = takeArgValue(argv, ++i, arg);
    else if (arg === '--timeout') args.timeout = Number(takeArgValue(argv, ++i, arg));
    else if (arg === '--delay-ms') args.delayMs = Number(takeArgValue(argv, ++i, arg));
    else if (arg === '--safe-random-delay') {
      args.delayMinMs = 5 * MINUTE_MS;
      args.delayMaxMs = 20 * MINUTE_MS;
    } else if (arg === '--delay-min-minutes') args.delayMinMs = Math.round(Number(takeArgValue(argv, ++i, arg)) * MINUTE_MS);
    else if (arg === '--delay-max-minutes') args.delayMaxMs = Math.round(Number(takeArgValue(argv, ++i, arg)) * MINUTE_MS);
    else if (arg === '--delay-min-ms') args.delayMinMs = Number(takeArgValue(argv, ++i, arg));
    else if (arg === '--delay-max-ms') args.delayMaxMs = Number(takeArgValue(argv, ++i, arg));
    else if (arg === '--resume') args.resume = true;
    else if (arg === '--dry-run') args.dryRun = true;
    else if (arg === '--no-search') args.search = false;
    else if (arg === '-h' || arg === '--help') args.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  return args;
}

function takeArgValue(argv, index, optionName) {
  const value = argv[index];
  if (value == null || value === '' || value.startsWith('--') || value === '-h') {
    throw new Error(`${optionName} requires a value`);
  }
  return value;
}

function splitAliases(value) {
  return String(value || '')
    .split(/[|,，;；\n\r\t]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function normalizeEntityType(value) {
  const raw = String(value || '').trim();
  const key = raw.toLowerCase();
  const map = new Map([
    ['person', 'person'],
    ['people', 'person'],
    ['human', 'person'],
    ['人', 'person'],
    ['人物', 'person'],
    ['人名', 'person'],
    ['专家', 'person'],
    ['company', 'company'],
    ['brand', 'company'],
    ['organization', 'company'],
    ['org', 'company'],
    ['公司', 'company'],
    ['机构', 'company'],
    ['品牌', 'company'],
    ['服务商', 'company'],
    ['product', 'product'],
    ['tool', 'product'],
    ['产品', 'product'],
    ['工具', 'product'],
    ['平台', 'product'],
  ]);
  return map.get(raw) || map.get(key) || raw;
}

function timestampId() {
  return new Date().toISOString().replace(/[-:]/g, '').replace(/\..+/, 'Z');
}

function safeId(value, fallback) {
  const cleaned = String(value || '').trim().replace(/[^a-zA-Z0-9._-]+/g, '-').replace(/^-+|-+$/g, '');
  return (cleaned || fallback).slice(0, 80);
}

function readQuestions(file, globalRepeat, globalTarget) {
  const raw = fs.readFileSync(path.resolve(file), 'utf8');
  const trimmed = raw.trim();
  let values;
  if (trimmed.startsWith('[')) {
    values = JSON.parse(trimmed);
  } else {
    values = raw.split(/\r?\n/).map((line) => line.trim()).filter((line) => line && !line.startsWith('#'));
  }
  if (!Array.isArray(values) || values.length === 0) {
    throw new Error('questions must contain at least one question');
  }
  return values.map((value, index) => {
    if (typeof value === 'string') {
      return {
        id: `q${String(index + 1).padStart(2, '0')}`,
        index: index + 1,
        question: value,
        repeat: globalRepeat,
        target: globalTarget || '',
      };
    }
    const question = String(value.question || value.prompt || '').trim();
    if (!question) throw new Error(`question object at index ${index} is missing question`);
    const repeat = value.repeat == null ? globalRepeat : Number(value.repeat);
    return {
      id: safeId(value.id || value.key, `q${String(index + 1).padStart(2, '0')}`),
      index: index + 1,
      question,
      repeat,
      target: String(value.target || globalTarget || '').trim(),
    };
  });
}

function validateOptions(options) {
  if (options.help) return;
  if (!options.questions) throw new Error('Missing --questions <file>');
  if (options.targetEntity && !options.entityType) {
    throw new Error('--target-entity requires --entity-type person/company/product or 人/公司/产品');
  }
  if (options.entityType && !['person', 'company', 'product'].includes(options.entityType)) {
    throw new Error('--entity-type must be person/company/product or 人/公司/产品');
  }
  if (!Number.isInteger(options.repeat) || options.repeat < 1 || options.repeat > 50) {
    throw new Error('--repeat must be an integer between 1 and 50');
  }
  if (!Number.isInteger(options.timeout) || options.timeout < 30 || options.timeout > 1200) {
    throw new Error('--timeout must be an integer between 30 and 1200');
  }
  if (!Number.isInteger(options.delayMs) || options.delayMs < 0) {
    throw new Error('--delay-ms must be a non-negative integer');
  }
  const hasRandomDelay = options.delayMinMs != null || options.delayMaxMs != null;
  if (hasRandomDelay) {
    if (options.delayMinMs == null || options.delayMaxMs == null) {
      throw new Error('Random delay requires both a minimum and a maximum. Use --safe-random-delay or pass both delay bounds.');
    }
    if (!Number.isInteger(options.delayMinMs) || !Number.isInteger(options.delayMaxMs)) {
      throw new Error('Random delay bounds must resolve to integer milliseconds');
    }
    if (options.delayMinMs < 0 || options.delayMaxMs < 0) {
      throw new Error('Random delay bounds must be non-negative');
    }
    if (options.delayMinMs > options.delayMaxMs) {
      throw new Error('Random delay minimum must be less than or equal to the maximum');
    }
    if (options.delayMaxMs > MAX_DELAY_MS) {
      throw new Error('Random delay maximum must be 24 hours or less');
    }
  }
  options.crawlerScript = path.resolve(options.crawlerScript);
  if (!options.dryRun && !fs.existsSync(options.crawlerScript)) {
    throw new Error(`Crawler script not found: ${options.crawlerScript}`);
  }
}

function makePlan(questions) {
  const plan = [];
  for (const item of questions) {
    if (!Number.isInteger(item.repeat) || item.repeat < 1 || item.repeat > 50) {
      throw new Error(`repeat for ${item.id} must be an integer between 1 and 50`);
    }
    for (let repeatIndex = 1; repeatIndex <= item.repeat; repeatIndex += 1) {
      plan.push({
        sample_id: `${item.id}-r${String(repeatIndex).padStart(2, '0')}`,
        question_id: item.id,
        question_index: item.index,
        repeat_index: repeatIndex,
        repeat_total: item.repeat,
        question: item.question,
        target: item.target,
      });
    }
  }
  return plan;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function formatDuration(ms) {
  if (ms < 1000) return `${ms}ms`;
  const seconds = Math.round(ms / 1000);
  if (seconds < 60) return `${seconds}s`;
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  if (!remainingSeconds) return `${minutes}m`;
  return `${minutes}m ${remainingSeconds}s`;
}

function delayStrategy(options) {
  if (options.delayMinMs != null && options.delayMaxMs != null) {
    return {
      mode: 'random',
      min_ms: options.delayMinMs,
      max_ms: options.delayMaxMs,
      min_minutes: options.delayMinMs / MINUTE_MS,
      max_minutes: options.delayMaxMs / MINUTE_MS,
    };
  }
  return {
    mode: 'fixed',
    delay_ms: options.delayMs,
    delay_minutes: options.delayMs / MINUTE_MS,
  };
}

function nextDelayMs(options) {
  if (options.delayMinMs == null || options.delayMaxMs == null) return options.delayMs;
  const span = options.delayMaxMs - options.delayMinMs;
  return options.delayMinMs + Math.floor(Math.random() * (span + 1));
}

function loadJsonIfValid(file) {
  try {
    const parsed = JSON.parse(fs.readFileSync(file, 'utf8'));
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}

function cleanText(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function reusableRawResult(existing, sample) {
  if (!existing?.ok) return { ok: false, reason: 'existing raw result had ok=false' };
  const answerText = cleanText(existing.answer?.text);
  if (!answerText) return { ok: false, reason: 'existing raw result has no answer text' };
  const existingQuestion = cleanText(existing.question);
  const sampleQuestion = cleanText(sample.question);
  if (existingQuestion && existingQuestion !== sampleQuestion) {
    return { ok: false, reason: 'existing raw result question does not match current plan' };
  }
  return { ok: true, reason: '' };
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function appendLog(file, text) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, text);
}

function runSample(options, run, sample) {
  return new Promise((resolve) => {
    const rawPath = path.join(run.dir, 'raw', `${sample.sample_id}.json`);
    const logPath = path.join(run.dir, 'logs', `${sample.sample_id}.log`);
    const relativeRawPath = path.relative(run.dir, rawPath);
    const relativeLogPath = path.relative(run.dir, logPath);

    if (options.resume && fs.existsSync(rawPath)) {
      const existing = loadJsonIfValid(rawPath);
      const reuse = existing ? reusableRawResult(existing, sample) : { ok: false, reason: 'existing raw result is not valid JSON' };
      if (reuse.ok) {
        resolve({
          ...sample,
          ok: true,
          status: 'done',
          reused: true,
          started_at: existing.collected_at || null,
          finished_at: existing.collected_at || null,
          duration_ms: 0,
          raw_path: relativeRawPath,
          log_path: relativeLogPath,
          error: '',
          result: existing,
        });
        return;
      }
      appendLog(logPath, `[resume skipped] ${reuse.reason}; rerunning sample.\n`);
    }

    const session = `yao-ds-${run.id}-${sample.sample_id}`.slice(0, 120);
    const childArgs = [
      options.crawlerScript,
      '--session',
      session,
      '--prompt',
      sample.question,
      '--timeout',
      String(options.timeout),
      '--out',
      rawPath,
    ];
    if (options.profile) childArgs.push('--profile', options.profile);
    if (sample.target) childArgs.push('--target', sample.target);
    if (!options.search) childArgs.push('--no-search');

    fs.rmSync(logPath, { force: true });
    appendLog(logPath, `$ node ${childArgs.map((arg) => JSON.stringify(arg)).join(' ')}\n\n`);

    const started = new Date();
    const child = spawn(process.execPath, childArgs, {
      cwd: path.resolve(path.dirname(options.crawlerScript), '..'),
      env: process.env,
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    child.stdout.on('data', (chunk) => appendLog(logPath, chunk.toString()));
    child.stderr.on('data', (chunk) => appendLog(logPath, chunk.toString()));
    child.on('error', (error) => {
      const finished = new Date();
      appendLog(logPath, `\n[spawn error] ${error.message}\n`);
      resolve({
        ...sample,
        ok: false,
        status: 'failed',
        started_at: started.toISOString(),
        finished_at: finished.toISOString(),
        duration_ms: finished.getTime() - started.getTime(),
        raw_path: relativeRawPath,
        log_path: relativeLogPath,
        error: error.message,
        result: null,
      });
    });
    child.on('close', (code) => {
      const finished = new Date();
      const result = loadJsonIfValid(rawPath);
      const ok = code === 0 && Boolean(result?.ok);
      resolve({
        ...sample,
        ok,
        status: ok ? 'done' : 'failed',
        started_at: started.toISOString(),
        finished_at: finished.toISOString(),
        duration_ms: finished.getTime() - started.getTime(),
        raw_path: relativeRawPath,
        log_path: relativeLogPath,
        error: ok ? '' : (result ? 'crawler returned ok=false' : `crawler exited with code ${code}`),
        result,
      });
    });
  });
}

function summarize(samples, planned) {
  const completed = samples.filter((sample) => sample.status === 'done' || sample.status === 'failed').length;
  const ok = samples.filter((sample) => sample.ok).length;
  const failed = samples.filter((sample) => sample.status === 'failed').length;
  const referenceCount = samples.reduce((sum, sample) => {
    const refs = sample.result?.references?.items || [];
    return sum + refs.length;
  }, 0);
  const answerChars = samples.reduce((sum, sample) => {
    const text = sample.result?.answer?.text || '';
    return sum + text.length;
  }, 0);
  return {
    planned_samples: planned.length,
    completed_samples: completed,
    ok_samples: ok,
    failed_samples: failed,
    valid_sample_rate: planned.length ? ok / planned.length : 0,
    reference_count: referenceCount,
    answer_chars: answerChars,
  };
}

function updateSampleTransports(dataset) {
  dataset.run.sample_transports = [...new Set(
    dataset.samples
      .map((sample) => String(sample.result?.transport || '').trim())
      .filter(Boolean),
  )].sort();
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }
  validateOptions(options);

  const crawlerTarget = options.target || options.targetEntity;
  const questions = readQuestions(options.questions, options.repeat, crawlerTarget);
  const plan = makePlan(questions);
  const runId = safeId(path.basename(options.outDir || ''), '') || `deepseek-${timestampId()}`;
  const outDir = path.resolve(options.outDir || path.join(skillRoot, 'runs', runId));
  const run = {
    id: runId,
    started_at: new Date().toISOString(),
    finished_at: null,
    engine: 'deepseek',
    transport: 'batch-orchestrator',
    sample_transports: [],
    crawler_script: options.crawlerScript,
    dir: outDir,
    dry_run: options.dryRun,
  };

  const dataset = {
    schema_version: 'yao-deepseek-crawler/v1',
    run,
    input: {
      question_count: questions.length,
      global_repeat: options.repeat,
      timeout: options.timeout,
      search: options.search,
      profile: options.profile || null,
      target_entity: options.targetEntity || null,
      target_aliases: options.targetAliases,
      entity_type: options.entityType || null,
      delay_strategy: delayStrategy(options),
      questions,
    },
    plan,
    samples: [],
    totals: summarize([], plan),
  };

  fs.mkdirSync(outDir, { recursive: true });
  writeJson(path.join(outDir, 'deepseek-crawl.json'), dataset);

  if (options.dryRun) {
    dataset.run.finished_at = new Date().toISOString();
    dataset.totals = summarize(dataset.samples, plan);
    writeJson(path.join(outDir, 'deepseek-crawl.json'), dataset);
    console.log(JSON.stringify({ ok: true, dry_run: true, out_dir: outDir, samples: plan.length }, null, 2));
    return;
  }

  for (let i = 0; i < plan.length; i += 1) {
    const sample = plan[i];
    console.error(`[${i + 1}/${plan.length}] ${sample.sample_id}`);
    const record = await runSample(options, run, sample);
    dataset.samples.push(record);
    updateSampleTransports(dataset);
    dataset.totals = summarize(dataset.samples, plan);
    writeJson(path.join(outDir, 'deepseek-crawl.json'), dataset);
    if (i < plan.length - 1 && !record.reused) {
      const delayMs = nextDelayMs(options);
      if (delayMs > 0) {
        const strategy = delayStrategy(options);
        const suffix = strategy.mode === 'random'
          ? ` (random range ${formatDuration(strategy.min_ms)}-${formatDuration(strategy.max_ms)})`
          : '';
        const message = `[delay] waiting ${formatDuration(delayMs)} before next sample${suffix}`;
        console.error(message);
        appendLog(path.join(outDir, 'batch.log'), `${new Date().toISOString()} ${message}\n`);
        await sleep(delayMs);
      }
    }
  }

  dataset.run.finished_at = new Date().toISOString();
  dataset.totals = summarize(dataset.samples, plan);
  writeJson(path.join(outDir, 'deepseek-crawl.json'), dataset);
  console.log(JSON.stringify({
    ok: true,
    out_dir: outDir,
    dataset: path.join(outDir, 'deepseek-crawl.json'),
    totals: dataset.totals,
  }, null, 2));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
