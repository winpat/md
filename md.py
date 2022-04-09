from collections import deque
from dataclasses import dataclass
from itertools import repeat
from typing import Callable, Iterable, Iterator


def take(n: int, iterator: Iterator[str]) -> List:
    return [next(iterator) for _ in range(n)]


def starts_with(text: deque, prefix: Iterable) -> bool:
    for t, p in zip(text, prefix):
        if t != p:
            return False
    return True


def pop_while(text: deque, predicate: Callable) -> str:
    popped = ""
    while text and predicate(text[0]):
        popped += text.popleft()
    return popped


def cut_prefix(text: deque, prefix) -> str:
    return pop_while(text, lambda c: c == prefix)


def consume_whitespace(text: deque) -> str:
    return pop_while(text, lambda c: c == " ")


def consume_line(text: deque) -> str:
    return pop_while(text, lambda c: c != "\n")


def pop(text: deque, char: str) -> str:
    if text[0] == char:
        return text.popleft()
    raise ValueError


class Token:
    pass


@dataclass
class Heading(Token):
    name: str
    level: int


def heading(text: deque) -> Heading:
    prefix = cut_prefix(text, "#")
    consume_whitespace(text)
    name = consume_line(text)
    return Heading(name, level=len(prefix))


@dataclass
class Line(Token):
    text: str


def line(text: str) -> Line:
    result = consume_line(text)
    return Line(text=result)


@dataclass
class List(Token):
    text: str
    level: int


def list(text: deque) -> List:
    indent_level = len(consume_whitespace(text))
    pop(text, "*")
    consume_whitespace(text)
    result = consume_line(text)
    pop(text, "\n")

    # A multi-line list needs to be at least indented by two space from the list
    # indicator (*).
    indent_prefix = take(indent_level + 2, repeat(" "))

    while starts_with(text, indent_prefix) and text[indent_level + 2].isalnum():
        consume_whitespace(text)
        # We replace new lines with an whitespace.
        result += " "
        result += consume_line(text)
        pop(text, "\n")

    return List(text=result, level=indent_level + 1)


@dataclass
class Block(Token):
    text: str
    type: str


def block(text: deque) -> Block:
    cut_prefix(text, "`")
    consume_whitespace(text)
    block_type = consume_line(text)
    pop(text, "\n")
    result = pop_while(text, lambda c: c != "`")
    cut_prefix(text, "`")
    return Block(text=result, type=block_type if block_type else None)


def md(text: str) -> Iterator[Token]:
    text = deque(text.strip(" "))
    while text:
        head = text[0]
        match head:
            case "\n":
                text.popleft()
            case "#":
                yield heading(text)
            case "*":
                yield list(text)
            case _ if starts_with(text, "```"):
                yield block(text)
            case head if head.isalnum():
                yield line(text)
