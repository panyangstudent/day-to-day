#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
account="us-stock-news-brief"

export FEISHU_APP_ID="$(security find-generic-password -a "$account" -s us-stock-news-brief.FEISHU_APP_ID -w)"
export FEISHU_APP_SECRET="$(security find-generic-password -a "$account" -s us-stock-news-brief.FEISHU_APP_SECRET -w)"
export FEISHU_RECEIVE_ID="$(security find-generic-password -a "$account" -s us-stock-news-brief.FEISHU_RECEIVE_ID -w)"
export FEISHU_RECEIVE_ID_TYPE="$(security find-generic-password -a "$account" -s us-stock-news-brief.FEISHU_RECEIVE_ID_TYPE -w)"

python3 "$skill_dir/scripts/send_feishu.py" \
  --mode app \
  --message-format card \
  --title "${1:-美股交易前早报}"
