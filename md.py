from collections import deque
from typing import NamedTuple
import re


class Header(NamedTuple):
    level: int
    text: str


def headers(lines):
    line = lines.popleft()
    match = re.search(r"^(#+)\s(.*)$", line)
    level = len(match.group(1))
    text = match.group(2).rstrip()
    return Header(level, text)


PATTERNS = {r"^#+\s.*$": headers}


def md(text):
    lines = deque(text.split("\n"))
    tokens = []
    while lines:
        head = lines[0]
        for pattern, parser in PATTERNS.items():
            if re.match(pattern, head):
                parsed = parser(lines)
                tokens.append(parsed)

    return tokens
