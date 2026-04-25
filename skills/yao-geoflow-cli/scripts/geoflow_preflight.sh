#!/usr/bin/env bash
set -euo pipefail

workspace="${1:-}"
config_path="${2:-}"

if [[ -z "$workspace" ]]; then
  echo "Usage: geoflow_preflight.sh <workspace> [config]" >&2
  exit 1
fi

cli_path="$workspace/bin/geoflow"

api_base_url="${GEOFLOW_BASE_URL:-}"
api_token="${GEOFLOW_API_TOKEN:-}"

if [[ ! -f "$cli_path" ]]; then
  if [[ -f "$workspace/artisan" && -f "$workspace/routes/api.php" ]]; then
    if [[ -z "$api_base_url" || -z "$api_token" ]]; then
      echo "Missing CLI: $cli_path" >&2
      echo "Laravel GEOFlow detected. Set GEOFLOW_BASE_URL and GEOFLOW_API_TOKEN to use API v1 fallback." >&2
      exit 1
    fi

    catalog_url="${api_base_url%/}/api/v1/catalog"
    if ! catalog_output="$(curl -sS --max-time 15 -H "Authorization: Bearer $api_token" -H "Accept: application/json" "$catalog_url" 2>&1)"; then
      printf '%s\n' "$catalog_output" >&2
      echo "Preflight failed. Could not reach API fallback catalog: $catalog_url" >&2
      exit 3
    fi

    if printf '%s' "$catalog_output" | grep -Eqi '"success"[[:space:]]*:[[:space:]]*false|token-invalid|invalid token|401|403|unauthorized|forbidden|未授权|无效或已过期'; then
      printf '%s\n' "$catalog_output" >&2
      echo "Preflight failed. API fallback token authentication failed." >&2
      exit 3
    fi

    echo "API fallback preflight OK: $catalog_url"
    printf '%s\n' "$catalog_output"
    exit 0
  fi

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
