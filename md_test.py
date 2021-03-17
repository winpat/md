import pytest
from md import md, Paragraph, Header, ListItem
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
    assert md(text) == [expected]


@pytest.mark.parametrize(
    "text", [("    "), (""), ("\n\n \n")],
)
def test_empty_lines(text):
    assert md(text) == []


def test_paragraph():
    assert md("Hello World!") == [Paragraph("Hello World!")]


@pytest.mark.parametrize(
    "text,expected",
    [
        ("* First item", ListItem(1, "First item")),
        ("  * Second level item", ListItem(2, "Second level item")),
        ("* First item\n  Second line", ListItem(1, "First item Second line")),
        ("    * Deep list\n      Second line", ListItem(3, "Deep list Second line")),
    ],
)
def test_list(text, expected):
    assert md(text) == [expected]


def test_md():

    text = """
# Heading 1

This is the first paragraph.

* First item
* Second item
  * Sub item
"""
    assert md(text) == [
        Header(level=1, text="Heading 1"),
        Paragraph(text="This is the first paragraph."),
        ListItem(level=1, text="First item"),
        ListItem(level=1, text="Second item"),
        ListItem(level=2, text="Sub item"),
    ]
