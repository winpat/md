"""A simple regex-based markdown parser.

We iterate over the lines from start to end. For every line we try to figure out
which parsing function we need to apply to it (header, text, etc.).

Then we apply the first matching parsing function. A parser can consume as many
lines as it wants, in the end it needs to return a parsed token.

"""
from collections import deque
from typing import NamedTuple
import re


class Header(NamedTuple):
    level: int
    text: str

class Paragraph(NamedTuple):
    text: str


def headers(lines):
    line = lines.popleft()
    match = re.search(r"^(#+)\s(.*)$", line)
    level = len(match.group(1))
    text = match.group(2).rstrip()
    return Header(level, text)


def empty_lines(lines):
    lines.popleft()

def paragraph(lines):
    return Paragraph(lines.popleft())


PATTERNS = {
    r"^\s*$": empty_lines,
    r"^#+\s.*$": headers,
    r"^.*$": paragraph
}


def md(text):
    lines = deque(text.split("\n"))
    tokens = []
    while lines:
        head = lines[0]
        for pattern, parser in PATTERNS.items():
            if re.match(pattern, head):
                if parsed := parser(lines):
                    tokens.append(parsed)
                break

    return tokens
