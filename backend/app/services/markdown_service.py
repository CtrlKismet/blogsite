"""Markdown rendering service using markdown-it-py."""

from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin


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
    return md


_md = _create_md()


def render_markdown(content: str) -> str:
    """Render Markdown text to HTML."""
    return _md.render(content)
