#!/usr/bin/env bash
set -euo pipefail

workspace="${1:-}"
config_path="${2:-}"

if [[ -z "$workspace" ]]; then
  echo "Usage: geoflow_preflight.sh <workspace> [config]" >&2
  exit 1
fi

cli_path="$workspace/bin/geoflow"

if [[ ! -f "$cli_path" ]]; then
  echo "Missing CLI: $cli_path" >&2
  exit 1
fi

if [[ -x "$cli_path" ]]; then
  runner=("$cli_path")
else
  runner=(php "$cli_path")
fi

config_hint=""
if [[ -n "$config_path" ]]; then
  printf -v config_hint ' --config %q' "$config_path"
fi

login_hint="${runner[*]}${config_hint} login --base-url <url> --username <admin>"
login_force_hint="${runner[*]}${config_hint} login --base-url <url> --username <admin> --force"

run_cli() {
  if [[ -n "$config_path" ]]; then
    "${runner[@]}" --config "$config_path" "$@"
  else
    "${runner[@]}" "$@"
  fi
}

if ! config_output="$(run_cli config show 2>&1)"; then
  printf '%s\n' "$config_output" >&2
  echo "Preflight failed. Could not read config. Run: ${login_hint}" >&2
  exit 2
fi

printf '%s\n' "$config_output"

if ! catalog_output="$(run_cli catalog 2>&1)"; then
  printf '%s\n' "$catalog_output" >&2

  if printf '%s' "$catalog_output" | grep -Eqi 'token-invalid|invalid token|token[^[:alpha:]]*(expired|invalid)|401|403|unauthorized|forbidden|未授权|无效或已过期'; then
    echo "Preflight failed. Config exists but token authentication failed. Run: ${login_force_hint}" >&2
  else
    echo "Preflight failed. Authenticated API access failed for a reason other than an obvious token problem. Inspect the error above before retrying login." >&2
  fi
  exit 3
fi

printf '%s\n' "$catalog_output"
