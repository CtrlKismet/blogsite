"""AI service for generating article tags and summaries."""

import json
import logging
from pathlib import Path

from openai import OpenAI

from app.config import settings

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
你是一个博客助手。给定一篇博客文章的 Markdown 内容，请分析并返回 JSON：

{
  "summary": "不超过15个字的摘要",
  "tags": ["标签1", "标签2"]
}

摘要规则：
- 不超过15个字
- 参考作者的文风和语气，用作者可能会用的方式概括
- 不要写"本文讲述了"之类的套话，直接用一句短语概括核心

标签规则：
- 优先从已有标签中选择（如果提供了已有标签列表）
- 如果没有合适的已有标签，可以创建新标签
- 每篇文章 1-3 个标签
- 标签应简洁，2-4个字

只返回 JSON，不要其他内容。\
"""


def generate_article_meta(
    content: str,
    title: str,
    existing_tags: list[str] | None = None,
) -> tuple[str, list[str]] | None:
    """Call AI to generate summary and tags for an article.

    Returns (summary, tag_names) or None on failure.
    """
    if not settings.ai_api_key or settings.ai_api_key == "your-api-key-here":
        logger.warning("AI API key not configured, skipping")
        return None

    client = OpenAI(base_url=settings.ai_base_url, api_key=settings.ai_api_key)

    # Truncate content to avoid huge token usage
    truncated = content[:4000] if len(content) > 4000 else content

    user_msg = f"文章标题: {title}\n\n"
    if existing_tags:
        user_msg += f"已有标签: {', '.join(existing_tags)}\n\n"
    user_msg += f"文章内容:\n{truncated}"

    try:
        resp = client.chat.completions.create(
            model=settings.ai_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,
            max_tokens=65536,
        )
        raw = resp.choices[0].message.content or ""
        # Strip markdown code fences if present
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

        data = json.loads(raw)
        summary = data.get("summary", "")
        tags = data.get("tags", [])

        if not isinstance(tags, list):
            tags = []
        tags = [str(t) for t in tags if t]

        logger.info("AI generated: summary=%s, tags=%s", summary[:40], tags)
        return summary, tags

    except Exception:
        logger.exception("AI meta generation failed for: %s", title)
        return None


def get_existing_tags() -> list[str]:
    """Fetch current tag names from DB."""
    from app.database import SessionLocal, Tag
    from sqlalchemy import select

    with SessionLocal() as session:
        tags = session.execute(select(Tag.name)).scalars().all()
        return list(tags)

