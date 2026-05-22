---
name: us-stock-news-brief
description: Prepare concise daily US stock market briefs for investors as a pre-trading checklist, including market regime, the few key themes that matter, headline triage, impact direction, relevant tickers/ETFs, macro and earnings catalysts, risk checks, and a final analytical investment conclusion. Use when the user asks for 美股早报, 美股新闻, daily market news, premarket brief, important news for US stock investors, trading day checklist, concise Feishu push, or recurring morning/evening market summaries.
---

# US Stock News Brief

## Core Rule

Always browse current sources before answering. Market news, prices, calendars, guidance, and policy events change quickly; never rely on memory for a daily brief. Cite source links for all material claims and clearly label inference as analysis.

## Workflow

1. Confirm date, timezone, and session context.
   - Default to the user's locale/timezone when known.
   - For a China-based US stock investor, interpret "早上" as the user's local morning and cover overnight US market action, after-hours news, and upcoming US premarket catalysts.
   - State exact dates when relative dates such as today, yesterday, or tonight could be ambiguous.

2. Gather reliable source material.
   - Prioritize primary or market-moving sources: SEC filings, company IR press releases, Federal Reserve, Treasury, BLS/BEA/Census, White House, court/regulator sites, exchange notices, earnings calendars, and official investor relations pages.
   - Use reputable newswires and market outlets for fast context: Reuters, AP, Bloomberg, CNBC, WSJ, Financial Times, MarketWatch, Investing.com, Nasdaq, NYSE, and major index/ETF data pages.
   - For China-related ADRs and geopolitics, include credible China/Asia and official sources when relevant.
   - Cross-check any surprising or high-impact claim with at least two sources when feasible.

3. Triage for investor relevance.
   - Lead with items likely to move indexes, rates, FX, commodities, or large sectors.
   - Include earnings and guidance from mega-cap, high-beta, index-heavy, or user-held names.
   - Include macro calendar items due in the next US session: CPI/PCE, payrolls, jobless claims, ISM/PMI, retail sales, FOMC speakers/minutes/decisions, Treasury auctions, crude inventory, and major geopolitical deadlines.
   - Deprioritize generic political or social news unless it has a plausible market transmission channel.
   - Convert the news flow into a trading-day checklist, not only a headline digest.

4. Analyze impact with discipline.
   - Separate facts, market reaction, and your interpretation.
   - Explain the transmission channel: rates, earnings revisions, margins, demand, regulation, supply chain, risk premium, positioning, or liquidity.
   - Use conditional language for uncertain outcomes. Avoid pretending to predict prices.
   - Call out what would invalidate the read.

5. Output in concise Chinese unless the user requests another language.
   - Keep it skimmable for a morning routine.
   - Prefer bullets and short labels.
   - Include links inline or in a compact source list.
   - For Feishu/mobile pushes, compress aggressively: target 700-1000 Chinese characters, maximum 4 key news items, no long background paragraphs.

## Recommended Output

Use `scripts/brief_template.py` to generate a clean structure when useful:

```bash
python3 /path/to/us-stock-news-brief/scripts/brief_template.py --date YYYY-MM-DD --timezone Asia/Shanghai --focus "美股投资者"
```

Fill the template with verified, cited information. For scheduled Feishu pushes, use this concise structure:

1. **市场结论**: One sentence summarizing risk appetite, dominant driver, and whether the setup is favorable, neutral, or defensive.
2. **三条主线**: Exactly 3 bullets. Each bullet should explain one market driver and the affected ETF/tickers.
3. **关键新闻**: Maximum 4 items. Each item must be one compact line with `事实 + 影响方向 + 相关标的 + 来源`.
4. **今晚/今日关注**: 2-4 time-sensitive macro, earnings, Fed, or geopolitical events.
5. **交易前检查**: 3 practical checks. Focus on yields, futures breadth, VIX, dollar, oil, earnings gaps, or event risk.
6. **投资结论**: Provide a clear analytical conclusion, not just "关注". Include:
   - `基准判断`: 偏多 / 中性 / 偏谨慎, with one reason.
   - `更适合`: The kind of exposure or setup that currently has better odds.
   - `不适合`: The behavior or exposure to avoid.
   - `反证条件`: What would change the conclusion.

Avoid dumping every source into the main body. Put compact source links at the end when needed.

## Style Guardrails

- Do not provide personalized financial advice unless the user gives portfolio context and explicitly asks; even then, frame as educational analysis and risk considerations.
- Do not say "buy", "sell", or "must" as a recommendation. Use "关注", "可能利好/利空", "需要验证", and "适合纳入观察".
- Prefer "what to watch" and "what would change the read" over direct trading instructions.
- The final investment conclusion should be directional and useful, but not a personalized order. Say what setup is favored, what should be avoided, and what would invalidate the view.
- Include a brief "不要做什么" warning when the market setup has obvious behavioral traps, such as chasing before earnings, ignoring rates, or overreacting to unverified headlines.
- When prices or futures are important, use finance/web tools to verify fresh values and name the timestamp or source.
- If source access is limited, say what could not be verified and reduce confidence.
- If the user asks to make this recurring, create an automation separately; the skill only defines the briefing workflow.

## Optional Reference

Read `references/market-impact-taxonomy.md` when the brief needs deeper sector mapping or when explaining why a headline matters.

## Feishu Delivery

When the user asks to send the brief to Feishu, use `scripts/send_feishu.py`. Prefer app mode with `--message-format card` for durable scheduled delivery and better mobile readability; use webhook mode for quick group-only setup.

Webhook mode: provide the webhook through `FEISHU_WEBHOOK_URL` or `--webhook-url`. If the Feishu bot has signature verification enabled, provide the secret through `FEISHU_WEBHOOK_SECRET` or `--secret`.

```bash
python3 scripts/send_feishu.py --mode webhook --title "美股交易前早报" --file brief.md
```

App bot mode: provide `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_RECEIVE_ID`, and `FEISHU_RECEIVE_ID_TYPE`. For group chats, `FEISHU_RECEIVE_ID` usually starts with `oc_` and `FEISHU_RECEIVE_ID_TYPE` should be `chat_id`.

```bash
python3 scripts/send_feishu.py --mode app --message-format card --title "美股交易前早报" --file brief.md
```

For generated content that is not saved to a file, pipe it through stdin:

```bash
printf '%s\n' "$BRIEF_MARKDOWN" | python3 scripts/send_feishu.py --mode app --message-format card --title "美股交易前早报"
```
