#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$skill_dir/.." && pwd)"
account="us-stock-news-brief"
env_file="$repo_dir/.env.feishu"

if [[ -f "$env_file" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$env_file"
  set +a
fi

read_keychain() {
  local service="$1"
  security find-generic-password -a "$account" -s "$service" -w 2>/dev/null || true
}

export FEISHU_APP_ID="${FEISHU_APP_ID:-$(read_keychain us-stock-news-brief.FEISHU_APP_ID)}"
export FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-$(read_keychain us-stock-news-brief.FEISHU_APP_SECRET)}"
export FEISHU_RECEIVE_ID="${FEISHU_RECEIVE_ID:-$(read_keychain us-stock-news-brief.FEISHU_RECEIVE_ID)}"
export FEISHU_RECEIVE_ID_TYPE="${FEISHU_RECEIVE_ID_TYPE:-$(read_keychain us-stock-news-brief.FEISHU_RECEIVE_ID_TYPE)}"

python3 "$skill_dir/scripts/send_feishu.py" \
  --mode app \
  --message-format card \
  --title "${1:-美股交易前早报}"
