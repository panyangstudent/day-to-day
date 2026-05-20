---
name: us-stock-news-brief
description: Prepare daily US stock market news briefs for investors, including premarket or morning headline triage, macro events, earnings, analyst/regulatory/company catalysts, sector impact, watchlists, and concise investment-risk analysis. Use when the user asks for 美股早报, 美股新闻, daily market news, premarket brief, important news for US stock investors, or recurring morning market summaries.
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

Fill the template with verified, cited information. A strong brief includes:

1. **一句话总览**: Market regime and top risk-on/risk-off driver.
2. **隔夜市场**: S&P 500, Nasdaq, Dow, Russell 2000, VIX, 10Y yield, DXY, oil, gold, BTC when relevant.
3. **今日最重要的 5-8 条新闻**: Each item should have `事实`, `为什么重要`, `可能受影响`, and `来源`.
4. **公司与财报焦点**: Mega-cap tech, semis, AI, banks, consumer, energy, healthcare, and user's watchlist if provided.
5. **宏观日历**: Upcoming releases/speeches/events with exact US and local times if available.
6. **风险雷达**: 2-4 risks or catalysts to monitor during the session.
7. **投资者待办**: Practical checks such as watchlist gaps, earnings dates, stop levels, position sizing, or whether to wait for data.

## Style Guardrails

- Do not provide personalized financial advice unless the user gives portfolio context and explicitly asks; even then, frame as educational analysis and risk considerations.
- Do not say "buy", "sell", or "must" as a recommendation. Use "关注", "可能利好/利空", "需要验证", and "适合纳入观察".
- When prices or futures are important, use finance/web tools to verify fresh values and name the timestamp or source.
- If source access is limited, say what could not be verified and reduce confidence.
- If the user asks to make this recurring, create an automation separately; the skill only defines the briefing workflow.

## Optional Reference

Read `references/market-impact-taxonomy.md` when the brief needs deeper sector mapping or when explaining why a headline matters.
