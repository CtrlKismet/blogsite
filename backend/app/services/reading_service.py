"""Estimate reading length from rendered prose, excluding code blocks and formulas."""

import math
import re
from html.parser import HTMLParser

_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0002ebef]")
_WORD_RE = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)
_BLOCKS = {"p", "div", "br", "li", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6"}
_VOID = {"br", "hr", "img", "input", "col", "wbr"}


class _ProseParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "") or ""
        ignored = tag in {"pre", "script", "style"} or "math" in classes.split()
        if self.ignored_depth or ignored:
            if tag not in _VOID:
                self.ignored_depth += 1
        elif tag in _BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if self.ignored_depth:
            if tag not in _VOID:
                self.ignored_depth -= 1
        if not self.ignored_depth and (tag in _BLOCKS or tag == "pre"):
            self.parts.append("\n")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in _VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if not self.ignored_depth:
            self.parts.append(data)


def reading_stats(content_html: str) -> tuple[int, int]:
    """Count Chinese characters and non-CJK words; estimate 300 units per minute."""
    parser = _ProseParser()
    parser.feed(content_html)
    parser.close()
    prose = "".join(parser.parts)
    count = len(_CJK_RE.findall(prose)) + len(_WORD_RE.findall(_CJK_RE.sub(" ", prose)))
    return count, max(1, math.ceil(count / 300))
