#!/usr/bin/env python3
"""Generate a reusable Markdown skeleton for a US stock market news brief."""

from __future__ import annotations

import argparse
from datetime import date


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a US stock news brief template.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Brief date, YYYY-MM-DD.")
    parser.add_argument("--timezone", default="Asia/Shanghai", help="Reader timezone.")
    parser.add_argument("--focus", default="美股投资者", help="Audience or portfolio focus.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"""# 美股交易前早报｜{args.date}

读者：{args.focus}
时区：{args.timezone}

## 市场温度计
- 市场结论：
- 风险偏好：
- 主导变量：

## 三条主线
1. 
2. 
3. 

## 关键新闻
1. **标题**：事实；影响方向；相关标的；来源。

## 今晚/今日关注
- 

## 交易前检查
- 

## 投资结论
- 基准判断：
- 更适合：
- 不适合：
- 反证条件：

## 来源
- 
""")


if __name__ == "__main__":
    main()
