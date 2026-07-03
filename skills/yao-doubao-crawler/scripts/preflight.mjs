#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const scriptDir = path.dirname(__filename);
const skillRoot = path.resolve(scriptDir, '..');
const defaultCrawlerScript = path.join(skillRoot, 'scripts', 'doubao_browser_crawl.mjs');

function printHelp() {
  console.log(`Usage:
  node scripts/preflight.mjs [options]

Options:
  --profile <name>          OpenCLI Browser Bridge profile to verify.
  --crawler-script <file>   Doubao browser crawler script. Default: scripts/doubao_browser_crawl.mjs.
  --analysis-only           Check only dependencies needed to analyze an existing crawl JSON.
  --timeout <seconds>       Timeout per OpenCLI check. Default: 30.
  --json                    Print machine-readable JSON.
  -h, --help                Show help.
`);
}

function parseArgs(argv) {
  const args = {
    profile: '',
    crawlerScript: process.env.DOUBAO_CRAWLER_SCRIPT || defaultCrawlerScript,
    analysisOnly: false,
    timeout: 30,
    json: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--profile') args.profile = argv[++i] || '';
    else if (arg === '--crawler-script') args.crawlerScript = argv[++i] || '';
    else if (arg === '--analysis-only') args.analysisOnly = true;
    else if (arg === '--timeout') args.timeout = Number(argv[++i]);
    else if (arg === '--json') args.json = true;
    else if (arg === '-h' || arg === '--help') args.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!Number.isInteger(args.timeout) || args.timeout < 5 || args.timeout > 300) {
    throw new Error('--timeout must be an integer between 5 and 300');
  }
  return args;
}

function parseVersion(text) {
  const match = String(text || '').match(/v?(\d+)\.(\d+)\.(\d+)/);
  if (!match) return null;
  return [Number(match[1]), Number(match[2]), Number(match[3])];
}

function versionAtLeast(version, minimum) {
  if (!version) return false;
  for (let i = 0; i < minimum.length; i += 1) {
    if (version[i] > minimum[i]) return true;
    if (version[i] < minimum[i]) return false;
  }
  return true;
}

function statusIcon(status) {
  return {
    pass: '[PASS]',
    warn: '[WARN]',
    fail: '[FAIL]',
    skip: '[SKIP]',
  }[status] || '[INFO]';
}

function compactOutput(value, maxLength = 900) {
  const text = String(value || '').trim();
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
}

function cleanCliOutput(value) {
  return String(value || '')
    .split(/\r?\n/)
    .filter((line) => !/^\(node:\d+\)/.test(line))
    .filter((line) => !/^\(Use `node --trace-warnings/.test(line))
    .join('\n')
    .trim();
}

function extractJsonObject(text) {
  const raw = String(text || '');
  try {
    const parsed = JSON.parse(raw.trim());
    if (Array.isArray(parsed)) return parsed[0] || null;
    return parsed;
  } catch {}
  const start = raw.indexOf('{');
  const end = raw.lastIndexOf('}');
  if (start < 0 || end < start) return null;
  try {
    return JSON.parse(raw.slice(start, end + 1));
  } catch {
    return null;
  }
}

function opencliArgs(profile, args) {
  return profile ? ['--profile', profile, ...args] : args;
}

async function run(command, args, timeoutSeconds) {
  try {
    const result = await execFileAsync(command, args, {
      timeout: timeoutSeconds * 1000,
      maxBuffer: 10 * 1024 * 1024,
    });
    return {
      ok: true,
      stdout: result.stdout || '',
      stderr: result.stderr || '',
      output: cleanCliOutput(`${result.stdout || ''}${result.stderr || ''}`),
    };
  } catch (error) {
    return {
      ok: false,
      stdout: error.stdout || '',
      stderr: error.stderr || '',
      output: cleanCliOutput(`${error.stdout || ''}${error.stderr || ''}`),
      message: error.message,
      code: error.code,
    };
  }
}

function add(checks, key, label, status, detail, fix = '') {
  checks.push({ key, label, status, detail: detail || '', fix: fix || '' });
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printHelp();
    return;
  }

  const checks = [];
  const nodeVersion = parseVersion(process.version);
  const nodeMinimum = [18, 0, 0];
  add(
    checks,
    'node',
    'Node.js',
    versionAtLeast(nodeVersion, nodeMinimum) ? 'pass' : 'fail',
    `${process.version}; required ${nodeMinimum.join('.')}+`,
    'Install or switch to a newer Node.js runtime before running the crawler.',
  );

  const analyzerPath = path.join(skillRoot, 'scripts', 'analyze_doubao_results.py');
  add(
    checks,
    'analyzer_script',
    'Analyzer script',
    fs.existsSync(analyzerPath) ? 'pass' : 'fail',
    path.relative(skillRoot, analyzerPath),
    'Reinstall or repair the yao-doubao-crawler skill package.',
  );

  const python = await run('python3', ['--version'], options.timeout);
  const pythonText = python.output || python.message;
  const pythonVersion = parseVersion(pythonText);
  add(
    checks,
    'python3',
    'Python 3',
    python.ok && versionAtLeast(pythonVersion, [3, 10, 0]) ? 'pass' : 'fail',
    python.ok ? pythonText : compactOutput(pythonText),
    'Install Python 3.10+ and make sure `python3 --version` works.',
  );

  if (options.analysisOnly) {
    add(checks, 'fresh_crawl_checks', 'Fresh crawl checks', 'skip', 'analysis-only mode skips OpenCLI, browser, Doubao login, and crawler script checks.');
  } else {
    const crawlerScript = path.resolve(options.crawlerScript);
    add(
      checks,
      'crawler_script',
      'Doubao crawler script',
      fs.existsSync(crawlerScript) ? 'pass' : 'fail',
      crawlerScript,
      'Pass --crawler-script <file>, set DOUBAO_CRAWLER_SCRIPT, or repair scripts/doubao_browser_crawl.mjs.',
    );

    const opencliVersion = await run('opencli', ['--version'], options.timeout);
    const opencliText = opencliVersion.output || opencliVersion.message;
    const parsedOpenCli = parseVersion(opencliText);
    add(
      checks,
      'opencli',
      'OpenCLI CLI',
      opencliVersion.ok && versionAtLeast(parsedOpenCli, [1, 8, 4]) ? 'pass' : 'fail',
      opencliVersion.ok ? opencliText : compactOutput(opencliText),
      'Install or update OpenCLI until `opencli --version` returns 1.8.4 or newer.',
    );

    if (opencliVersion.ok) {
      const doctor = await run('opencli', opencliArgs(options.profile, ['doctor']), options.timeout);
      const doctorText = doctor.output || doctor.message;
      const doctorConnected = doctor.ok
        && /Extension:\s*connected|Everything looks good/i.test(doctorText)
        && !/No Browser Bridge profiles connected|not connected|\[FAIL\]|\[MISSING\]/i.test(doctorText);
      add(
        checks,
        'browser_bridge',
        'Browser Bridge',
        doctorConnected ? 'pass' : 'fail',
        doctorConnected ? `connected${options.profile ? ` via ${options.profile}` : ''}` : compactOutput(doctorText),
        'Open a Chrome/Edge profile with the OpenCLI Browser Bridge extension enabled, then rerun `opencli doctor`.',
      );

      const profiles = await run('opencli', ['profile', 'list'], options.timeout);
      const profileText = profiles.output || profiles.message;
      const hasConnectedProfile = profiles.ok && /connected/i.test(profileText) && !/No Browser Bridge profiles connected/i.test(profileText);
      const requestedProfileOk = !options.profile || new RegExp(`\\b${options.profile.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b[\\s\\S]*connected|connected[\\s\\S]*\\b${options.profile.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i').test(profileText);
      add(
        checks,
        'profile',
        'OpenCLI profile',
        hasConnectedProfile && requestedProfileOk ? 'pass' : 'fail',
        hasConnectedProfile && requestedProfileOk
          ? (options.profile ? `${options.profile} connected` : compactOutput(profileText))
          : compactOutput(profileText),
        options.profile
          ? `Connect profile ${options.profile}, or choose a connected profile with \`opencli profile use <profile>\`.`
          : 'Connect at least one Browser Bridge profile before crawling.',
      );

      const status = await run('opencli', opencliArgs(options.profile, ['doubao', 'status', '-f', 'json']), options.timeout);
      const statusText = status.output || status.message;
      const statusJson = extractJsonObject(statusText);
      const statusUrl = String(statusJson?.Url ?? statusJson?.url ?? '');
      add(
        checks,
        'doubao_adapter',
        'Doubao adapter',
        status.ok ? 'pass' : 'fail',
        statusJson ? JSON.stringify(statusJson) : compactOutput(statusText),
        'Verify the OpenCLI doubao adapter with `opencli doubao status -f json`.',
      );
      add(
        checks,
        'doubao_region_access',
        'Doubao region access',
        /region-ban/i.test(statusUrl) ? 'fail' : (status.ok ? 'pass' : 'skip'),
        statusUrl || 'No Doubao page URL reported.',
        'Open Doubao from a browser/network location where https://www.doubao.com is available, then rerun preflight.',
      );

      const whoami = await run('opencli', opencliArgs(options.profile, ['doubao', 'whoami', '-f', 'json']), options.timeout);
      const whoamiText = whoami.output || whoami.message;
      const whoamiJson = extractJsonObject(whoamiText);
      const statusLoginYes = /yes|true/i.test(String(statusJson?.Login ?? statusJson?.login ?? ''));
      add(
        checks,
        'doubao_login',
        'Doubao login',
        whoami.ok && whoamiJson?.logged_in === true ? 'pass' : (statusLoginYes ? 'warn' : 'fail'),
        whoami.ok && whoamiJson
          ? JSON.stringify({ logged_in: whoamiJson.logged_in, site: whoamiJson.site })
          : `${statusLoginYes ? 'status reports Login=Yes; whoami did not expose a session cookie. ' : ''}${compactOutput(whoamiText)}`,
        statusLoginYes
          ? 'Basic Doubao sending may still work. If account-specific features fail, refresh Doubao login and verify with `opencli doubao whoami -f json`.'
          : 'Log in to Doubao in the connected browser, or run `opencli doubao login --timeout 180`, then verify with `opencli doubao whoami -f json`.',
      );
    } else {
      add(checks, 'browser_bridge', 'Browser Bridge', 'skip', 'Skipped because OpenCLI is unavailable.');
      add(checks, 'profile', 'OpenCLI profile', 'skip', 'Skipped because OpenCLI is unavailable.');
      add(checks, 'doubao_login', 'Doubao login', 'skip', 'Skipped because OpenCLI is unavailable.');
    }
  }

  const failed = checks.filter((check) => check.status === 'fail');
  const warnings = checks.filter((check) => check.status === 'warn');
  const result = {
    ok: failed.length === 0,
    mode: options.analysisOnly ? 'analysis-only' : 'fresh-crawl',
    profile: options.profile || null,
    crawler_script: options.analysisOnly ? null : path.resolve(options.crawlerScript),
    checks,
  };

  if (options.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`Yao Doubao Crawler preflight (${result.mode})`);
    console.log('');
    for (const check of checks) {
      console.log(`${statusIcon(check.status)} ${check.label}: ${check.detail}`);
      if (check.status === 'fail' && check.fix) console.log(`       Fix: ${check.fix}`);
    }
    console.log('');
    if (result.ok) {
      console.log('Ready: preflight passed.');
    } else {
      console.log(`Not ready: ${failed.length} failed check(s), ${warnings.length} warning(s).`);
    }
  }

  process.exitCode = result.ok ? 0 : 1;
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
