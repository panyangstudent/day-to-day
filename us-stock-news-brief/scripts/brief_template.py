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
- 风险偏好：
- 今日主线：
- 关键变量：
- 利率压力：
- 波动风险：

## 今日三大主线
1. 
2. 
3. 

## 重点新闻与影响分析
1. **标题**
   - 事实：
   - 影响方向：
   - 影响周期：
   - 为什么重要：
   - 相关标的：
     - 直接影响：
     - 间接影响：
     - 反向关注：
   - 反证/观察点：
   - 置信度：
   - 来源：

## 公司/财报雷达
- 

## 宏观日历
- 

## 相关 ETF / 股票观察池
- 直接影响：
- 间接影响：
- 反向关注：

## 今日交易前检查清单
- 

## 风险与反证
- 
- 不要做什么：

## 来源
- 
""")


if __name__ == "__main__":
    main()
