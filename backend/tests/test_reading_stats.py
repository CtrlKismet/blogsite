from app.services.markdown_service import render_markdown
from app.services.reading_service import reading_stats


def test_mixed_chinese_and_english():
    assert reading_stats("<p>你好，Vue and Python！</p>") == (5, 1)


def test_markdown_counts_prose_but_not_code_urls_or_formulas():
    html = render_markdown(
        "# 标题\n\n阅读 [文档](https://example.com/long/path)。\n\n"
        "```python\nprint('many code words')\n```\n\n$x + y$\n"
    )
    assert reading_stats(html) == (6, 1)


def test_inline_markup_and_html_entities():
    assert reading_stats("<p>Hel<strong>lo</strong> &amp; world.</p><p>Next</p>") == (3, 1)


def test_reading_minutes_round_up_and_have_minimum():
    assert reading_stats("") == (0, 1)
    assert reading_stats("文" * 300) == (300, 1)
    assert reading_stats("文" * 301) == (301, 2)


def test_nested_ignored_elements_do_not_hide_following_prose():
    assert reading_stats("<pre><code>ignored<br />words</code></pre><p>正文</p>") == (2, 1)
