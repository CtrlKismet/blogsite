from html.parser import HTMLParser

import pytest

from app.services.markdown_service import render_markdown
from app.services.reading_service import reading_stats


class CodeText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_code = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "code":
            self.in_code = True

    def handle_endtag(self, tag):
        if tag == "code":
            self.in_code = False

    def handle_data(self, data):
        if self.in_code:
            self.parts.append(data)


@pytest.mark.parametrize("language,code", [
    ("python", 'def greet():\n    return "你好"\n'),
    ("js", 'const message = "hello";\n'),
    ("bash", 'echo "hello"\n'),
    ("json", '{"enabled": true}\n'),
    ("yaml", 'enabled: true\n'),
])
def test_common_languages_are_highlighted_and_copy_text_is_preserved(language, code):
    html = render_markdown(f"```{language}\n{code}```\n")
    assert 'class="syntax-' in html
    assert f'language-{language}' in html
    parser = CodeText()
    parser.feed(html)
    assert "".join(parser.parts) == code
    assert reading_stats(html) == (0, 1)


@pytest.mark.parametrize("language", ["", "unknown-language", "html"])
def test_html_inside_code_is_escaped(language):
    code = '<script>alert("hello")</script>\n'
    html = render_markdown(f"```{language}\n{code}```\n")
    assert "<script>" not in html
    parser = CodeText()
    parser.feed(html)
    assert "".join(parser.parts) == code


def test_blank_lines_indentation_and_inline_code_are_preserved():
    code = '\n    value = "<example>"\n\n'
    html = render_markdown(f"```python\n{code}```\n\n`inline`\n")
    parser = CodeText()
    parser.feed(html)
    assert "".join(parser.parts) == code + "inline"
    assert "<code>inline</code>" in html
