---
name: us-stock-news-brief
description: Prepare daily US stock market morning briefs for investors as a pre-trading checklist, including market regime, key themes, headline triage, impact direction, relevant tickers/ETFs, macro events, earnings catalysts, risk checks, and concise investment-risk analysis. Use when the user asks for 美股早报, 美股新闻, daily market news, premarket brief, important news for US stock investors, trading day checklist, or recurring morning market summaries.
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

## Recommended Output

Use `scripts/brief_template.py` to generate a clean structure when useful:

```bash
python3 /path/to/us-stock-news-brief/scripts/brief_template.py --date YYYY-MM-DD --timezone Asia/Shanghai --focus "美股投资者"
```

Fill the template with verified, cited information. A strong brief uses this structure:

1. **市场温度计**: A 10-second dashboard with `风险偏好`, `主线`, `今日关键变量`, `利率压力`, and `波动风险`.
2. **今日三大主线**: The three narratives most likely to drive US equities today, each with a one-line market implication.
3. **重点新闻与影响分析**: 5-8 investor-relevant items. Each item should include:
   - `事实`: What happened, with a source.
   - `影响方向`: 利好 / 利空 / 中性 / 双刃剑.
   - `影响周期`: 盘前 / 日内 / 本周 / 中期.
   - `为什么重要`: Transmission channel such as rates, earnings, margins, liquidity, regulation, positioning, or sentiment.
   - `相关标的`: Split into `直接影响`, `间接影响`, and `反向关注` when useful.
   - `反证/观察点`: What would weaken or confirm the analysis.
   - `置信度`: High / Medium / Low.
4. **公司/财报雷达**: Earnings, guidance, analyst day, product launches, regulatory events, and after-hours catalysts for mega-cap, AI, semis, banks, consumer, energy, healthcare, and user watchlist names.
5. **宏观日历**: Upcoming releases/speeches/events with exact US and local times if available.
6. **相关 ETF / 股票观察池**: Group tickers into `直接影响`, `间接影响`, and `反向关注` buckets. Include broad ETFs such as SPY, QQQ, IWM, DIA, SMH, XLF, XLE, XLY, XLV, TLT, UUP, GLD when relevant.
7. **今日交易前检查清单**: 3-6 concrete premarket checks, such as yields, futures breadth, VIX, dollar, oil, earnings gaps, and whether a position has event risk.
8. **风险与反证**: Explain the top ways the morning thesis could be wrong, plus what data or price action would change the read.

## Style Guardrails

- Do not provide personalized financial advice unless the user gives portfolio context and explicitly asks; even then, frame as educational analysis and risk considerations.
- Do not say "buy", "sell", or "must" as a recommendation. Use "关注", "可能利好/利空", "需要验证", and "适合纳入观察".
- Prefer "what to watch" and "what would change the read" over direct trading instructions.
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
