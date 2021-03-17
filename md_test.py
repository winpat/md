from md import md


def test_md():

    text = """
# Heading 1

This is some text with **bold** text. This text stretches across multiple lines,
which is pretty cool.

* It also has a list
* With two elements
"""

    assert md(text) == []
