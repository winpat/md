from md import Block, Heading, Line, List, md

TEXT = """
# Title 1

This is some line!

* List item 1

* Cool story this so cool we will continue
  on the next line.

This is some code:

```python
def main():
    pass
```

```
(message "cool")
```

"""


def test_md():
    assert list(md(TEXT)) == [
        Heading(name="Title 1", level=1),
        Line(text="This is some line!"),
        List(text="List item 1", level=1),
        List(
            text="Cool story this so cool we will continue on the next line.", level=1
        ),
        Line(text="This is some code:"),
        Block(text="def main():\n    pass\n", type="python"),
        Block(text='(message "cool")\n', type=None),
    ]
