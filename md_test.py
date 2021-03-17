import pytest
from md import md, headers, Header
from collections import deque


@pytest.mark.parametrize(
    "text,expected",
    [
        ("# Heading 1", Header(1, "Heading 1")),
        ("# 1994", Header(1, "1994")),
        ("## Subheading 1", Header(2, "Subheading 1")),
        ("##### Why so many titles?", Header(5, "Why so many titles?")),
    ],
)
def test_headers(text, expected):
    assert headers(deque([text])) == expected


def test_md():

    text = """# Heading 1 """

    assert md(text) == [Header(level=1, text="Heading 1")]
