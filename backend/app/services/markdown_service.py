"""Markdown rendering service using markdown-it-py."""

import re

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.footnote import footnote_plugin

# HTML block-level tags that need blank-line separation in CommonMark
_BLOCK_TAGS = (
    r"div|table|pre|blockquote|ol|ul|p|h[1-6]|hr|form|fieldset"
    r"|address|article|aside|details|figcaption|figure|footer"
    r"|header|hgroup|main|nav|section|summary"
)


def _preprocess_markdown(content: str) -> str:
    """Pre-process markdown to fix common CommonMark edge cases.

    1. Ensure ``$$`` display-math blocks have blank lines around them so that
       ``dollarmath_plugin`` recognises them as *block*-level math.
    2. Ensure a blank line follows HTML block-level closing tags (e.g.
       ``</div>``) so that subsequent Markdown (headings, paragraphs …) is
       parsed correctly instead of being swallowed by the HTML block.
    3. Convert Markdown image syntax ``![alt](url)`` inside HTML block-level
       tags to ``<img>`` tags so they render inside HTML blocks.
    4. Add blank line before tab-indented ordered list items so that
       CommonMark recognises them as nested ordered lists.
    """
    # --- 1. $$ display-math blocks ---
    # Match paired $$ on their own lines with content in between
    content = re.sub(
        r"(^[ \t]*\$\$[ \t]*\n)(.*?\n)([ \t]*\$\$[ \t]*$)",
        lambda m: "\n" + m.group(0) + "\n",
        content,
        flags=re.MULTILINE | re.DOTALL,
    )

    # --- 2. Blank line after HTML block-level closing tags ---
    content = re.sub(
        rf"(</(?:{_BLOCK_TAGS})>[ \t]*)\n(?!\n)",
        r"\1\n\n",
        content,
        flags=re.IGNORECASE,
    )

    # --- 3. Markdown images inside HTML block-level tags ---
    # e.g. <div align=center>![alt](url)</div> → <div ...><img src="url" alt="alt"></div>
    content = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda m: (
            f'<img src="{m.group(2)}" alt="{m.group(1)}">'
            if re.search(
                rf"<(?:{_BLOCK_TAGS})\b",
                m.string[max(0, m.start() - 200) : m.start()],
                re.IGNORECASE,
            )
            else m.group(0)
        ),
        content,
    )

    # --- 4. Tab-indented ordered list nesting ---
    # In CommonMark, \t<num>. after a list item without a blank line is
    # treated as continuation text.  Adding a blank line forces nested parsing.
    content = re.sub(r"(\n)(\t+\d+\.\s)", r"\1\n\2", content)

    # Collapse 3+ consecutive blank lines into 2
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content


def _create_md() -> MarkdownIt:
    """Create a configured markdown-it instance."""
    md = MarkdownIt(
        "commonmark",
        {
            "html": True,
            "breaks": True,
            "linkify": False,
            "typographer": False,
        },
    )
    # Enable common extensions
    md.enable(["table", "strikethrough"])
    # Footnotes
    footnote_plugin(md)
    # LaTeX math: $...$ inline, $$...$$ display
    dollarmath_plugin(md)
    return md


_md = _create_md()


def _postprocess_html(html: str) -> str:
    """Post-process rendered HTML to fix remaining edge cases.

    Convert leftover ``~~text~~`` (which the strikethrough plugin failed to
    match due to delimiter-flanking rules) into ``<del>text</del>``.
    """
    if "~~" in html:
        html = re.sub(r"~~(.+?)~~", r"<del>\1</del>", html)
    return html


def render_markdown(content: str) -> str:
    """Render Markdown text to HTML."""
    html = _md.render(_preprocess_markdown(content))
    return _postprocess_html(html)
