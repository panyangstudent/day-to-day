# Day To Day

This repository contains a Codex skill for preparing concise US stock market briefs and optionally pushing them to Feishu/Lark.

## What It Does

- Defines the `us-stock-news-brief` skill for Chinese US-stock investor morning briefs.
- Generates a reusable Markdown brief skeleton.
- Sends a Markdown brief to Feishu by webhook bot or app bot.
- Includes a market-impact taxonomy for mapping news into macro, sector, ETF, and ticker implications.

## Files

- `us-stock-news-brief/SKILL.md`: skill workflow, output format, and Feishu delivery guidance.
- `us-stock-news-brief/scripts/brief_template.py`: creates a Markdown brief template.
- `us-stock-news-brief/scripts/send_feishu.py`: sends a brief to Feishu/Lark.
- `us-stock-news-brief/scripts/send_feishu_from_keychain.sh`: sends through app bot mode using `.env.feishu` or macOS Keychain values.
- `us-stock-news-brief/references/market-impact-taxonomy.md`: analysis reference for market impact.

## Generate A Brief Template

```bash
python3 us-stock-news-brief/scripts/brief_template.py \
  --date 2026-05-24 \
  --timezone Asia/Shanghai \
  --focus "美股投资者"
```

## Configure Feishu

Copy `.env.example` to `.env.feishu` and fill in either webhook or app bot values. `.env.*` files are ignored by git.

Webhook mode needs:

```bash
FEISHU_MODE=webhook
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/...
FEISHU_WEBHOOK_SECRET=
```

App bot mode needs:

```bash
FEISHU_MODE=app
FEISHU_MESSAGE_FORMAT=card
FEISHU_APP_ID=cli_...
FEISHU_APP_SECRET=...
FEISHU_RECEIVE_ID=oc_...
FEISHU_RECEIVE_ID_TYPE=chat_id
```

## Send To Feishu

Dry run first to validate the message payload without sending:

```bash
python3 us-stock-news-brief/scripts/send_feishu.py \
  --mode app \
  --message-format card \
  --title "美股交易前早报" \
  --file brief.md \
  --dry-run
```

Send through webhook mode:

```bash
python3 us-stock-news-brief/scripts/send_feishu.py \
  --mode webhook \
  --title "美股交易前早报" \
  --file brief.md
```

Send through app bot mode:

```bash
python3 us-stock-news-brief/scripts/send_feishu.py \
  --mode app \
  --message-format card \
  --title "美股交易前早报" \
  --file brief.md
```

If credentials are stored in `.env.feishu` or the macOS Keychain helper values, pipe content into:

```bash
printf '%s\n' "$BRIEF_MARKDOWN" | us-stock-news-brief/scripts/send_feishu_from_keychain.sh "美股交易前早报"
```
