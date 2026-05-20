#!/usr/bin/env python3
"""Send a Markdown market brief to Feishu/Lark.

Supports two delivery modes:
- webhook: incoming group bot webhook
- app: Feishu app bot using app_id/app_secret and receive_id
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a brief to Feishu.")
    parser.add_argument("--mode", choices=("webhook", "app"), default=os.environ.get("FEISHU_MODE", "webhook"))
    parser.add_argument(
        "--message-format",
        choices=("card", "post"),
        default=os.environ.get("FEISHU_MESSAGE_FORMAT", "card"),
        help="Feishu message format. card is easier to read on mobile.",
    )
    parser.add_argument("--title", default="美股交易前早报", help="Message title.")
    parser.add_argument("--file", help="Markdown file to send. Defaults to stdin.")
    parser.add_argument("--webhook-url", default=os.environ.get("FEISHU_WEBHOOK_URL"))
    parser.add_argument("--secret", default=os.environ.get("FEISHU_WEBHOOK_SECRET"))
    parser.add_argument("--app-id", default=os.environ.get("FEISHU_APP_ID"))
    parser.add_argument("--app-secret", default=os.environ.get("FEISHU_APP_SECRET"))
    parser.add_argument("--receive-id", default=os.environ.get("FEISHU_RECEIVE_ID"))
    parser.add_argument("--receive-id-type", default=os.environ.get("FEISHU_RECEIVE_ID_TYPE", "chat_id"))
    return parser.parse_args()


def read_content(path: str | None) -> str:
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    return sys.stdin.read().strip()


def sign(timestamp: str, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(string_to_sign, b"", digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def build_webhook_payload(title: str, content: str, secret: str | None) -> dict:
    payload = {"msg_type": "post", "content": build_post_content(title, content)}
    if secret:
        timestamp = str(int(time.time()))
        payload["timestamp"] = timestamp
        payload["sign"] = sign(timestamp, secret)
    return payload


def build_post_content(title: str, content: str) -> dict:
    return {
        "post": {
            "zh_cn": {
                "title": title,
                "content": [[{"tag": "text", "text": content}]],
            }
        }
    }


def post_json(url: str, payload: dict, headers: dict | None = None) -> dict:
    context = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or certifi_cafile())
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20, context=context) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Feishu HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Feishu request failed: {exc}") from exc

    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"raw": body}


def certifi_cafile() -> str | None:
    try:
        import certifi
    except ImportError:
        return None
    return certifi.where()


def send_webhook(webhook_url: str, payload: dict) -> None:
    parsed = post_json(webhook_url, payload)

    if parsed.get("code") not in (0, None):
        raise SystemExit(f"Feishu webhook returned error: {json.dumps(parsed, ensure_ascii=False)}")
    print("Sent to Feishu.")


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    parsed = post_json(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    if parsed.get("code") != 0 or not parsed.get("tenant_access_token"):
        raise SystemExit(f"Failed to get tenant_access_token: {json.dumps(parsed, ensure_ascii=False)}")
    return parsed["tenant_access_token"]


def build_app_message(title: str, content: str, message_format: str) -> dict:
    if message_format == "card":
        return {
            "msg_type": "interactive",
            "content": json.dumps(build_card_content(title, content), ensure_ascii=False),
        }
    return {
        "msg_type": "post",
        "content": json.dumps(build_post_content(title, content)["post"], ensure_ascii=False),
    }


def build_card_content(title: str, content: str) -> dict:
    sections = split_markdown_sections(content)
    elements: list[dict] = []

    lead = sections.pop("_lead", "")
    if lead:
        elements.append(markdown_block(lead, compact=True))

    for section_title in [
        "市场温度计",
        "今日三大主线",
        "重点新闻与影响分析",
        "公司/财报雷达",
        "宏观日历",
        "相关 ETF / 股票观察池",
        "今日交易前检查清单",
        "风险与反证",
        "来源",
    ]:
        body = sections.pop(section_title, "")
        if not body:
            continue
        if elements:
            elements.append({"tag": "hr"})
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"**{section_title}**"}})
        elements.extend(section_blocks(body))

    for section_title, body in sections.items():
        if elements:
            elements.append({"tag": "hr"})
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"**{section_title}**"}})
        elements.extend(section_blocks(body))

    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "blue",
            "title": {"tag": "plain_text", "content": title},
        },
        "elements": elements or [markdown_block(content, compact=True)],
    }


def split_markdown_sections(content: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current = "_lead"
    buffer: list[str] = []
    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        match = re.match(r"^#{1,3}\s+(.+)$", line)
        if match:
            if buffer:
                sections[current] = "\n".join(buffer).strip()
            current = match.group(1).strip()
            buffer = []
        else:
            buffer.append(line)
    if buffer:
        sections[current] = "\n".join(buffer).strip()
    return {key: value for key, value in sections.items() if value}


def section_blocks(body: str) -> list[dict]:
    chunks = chunk_text(body, 1200)
    return [markdown_block(chunk, compact=False) for chunk in chunks]


def markdown_block(text: str, compact: bool) -> dict:
    normalized = normalize_markdown_for_lark(text)
    if compact:
        normalized = normalized.strip()
    return {"tag": "div", "text": {"tag": "lark_md", "content": normalized}}


def normalize_markdown_for_lark(text: str) -> str:
    text = re.sub(r"^\s*-\s+", "• ", text, flags=re.MULTILINE)
    return text.strip()


def chunk_text(text: str, max_len: int) -> list[str]:
    lines = text.strip().splitlines()
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for line in lines:
        line_len = len(line) + 1
        if current and current_len + line_len > max_len:
            chunks.append("\n".join(current).strip())
            current = [line]
            current_len = line_len
        else:
            current.append(line)
            current_len += line_len
    if current:
        chunks.append("\n".join(current).strip())
    return chunks


def send_app(
    app_id: str,
    app_secret: str,
    receive_id: str,
    receive_id_type: str,
    title: str,
    content: str,
    message_format: str,
) -> None:
    token = get_tenant_access_token(app_id, app_secret)
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
    payload = {"receive_id": receive_id, **build_app_message(title, content, message_format)}
    parsed = post_json(url, payload, {"Authorization": f"Bearer {token}"})
    if parsed.get("code") != 0:
        raise SystemExit(f"Feishu app message returned error: {json.dumps(parsed, ensure_ascii=False)}")
    print("Sent to Feishu.")


def main() -> None:
    args = parse_args()
    content = read_content(args.file)
    if not content:
        raise SystemExit("No content to send.")

    if args.mode == "webhook":
        if not args.webhook_url:
            raise SystemExit("Missing FEISHU_WEBHOOK_URL or --webhook-url.")
        send_webhook(args.webhook_url, build_webhook_payload(args.title, content, args.secret))
        return

    if args.receive_id_type.startswith(("oc_", "ou_", "on_")) and not args.receive_id:
        raise SystemExit(
            "FEISHU_RECEIVE_ID_TYPE looks like an ID. Use FEISHU_RECEIVE_ID=oc_... "
            "and FEISHU_RECEIVE_ID_TYPE=chat_id."
        )
    missing = [
        name
        for name, value in {
            "FEISHU_APP_ID": args.app_id,
            "FEISHU_APP_SECRET": args.app_secret,
            "FEISHU_RECEIVE_ID": args.receive_id,
            "FEISHU_RECEIVE_ID_TYPE": args.receive_id_type,
        }.items()
        if not value
    ]
    if missing:
        raise SystemExit(f"Missing required app mode settings: {', '.join(missing)}")
    send_app(
        args.app_id,
        args.app_secret,
        args.receive_id,
        args.receive_id_type,
        args.title,
        content,
        args.message_format,
    )


if __name__ == "__main__":
    main()
