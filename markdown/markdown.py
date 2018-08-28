"""This is an exercise from https://exercism.io/my/tracks/python."""
import re
from typing import Tuple


def parse_markdown(markdown: str) -> str:
    """Very basic Markdown -> HTML parser."""
    html = ""
    in_list = False
    for line in markdown.split('\n'):
        # Better keep each markdown -> HTML encspsulated in subfunction:
        line, title_matched = parse_title(line)
        line = parse_all_bold(line)
        line = parse_all_emphasis(line)
        line, in_list = parse_list_item(line, in_list)
        if not (title_matched or in_list):
            line = html_node("p", line)
        html += line
    if in_list:
        html += "</ul>"
    return html


def html_node(markup: str, content: str) -> str:
    """Returns an HTML node of `markup` type with `content` as child."""
    return "<{0}>{1}</{0}>".format(markup, content)


TITLE_PATTERN = re.compile(r"([#]+)([^#]*)")

BOLD_PATTERN = re.compile(r"__(.*?)__")  # .*? stands for "any caracters" in a non-greedy way
BOLD_REPLACEMENT = html_node("strong", r"\1")
EM_PATTERN = re.compile(r"_(.*?)_")
EM_REPLACEMENT = html_node("em", r"\1")
LIST_PATTERN = re.compile(r"\* (.*)")


# Using subfunction to parse each type of input makes the whole thing easier to read.
def parse_title(line: str) -> Tuple[str, bool]:
    """Returns <hi>`text`</hi> if input string is an i-depth markdown title."""
    match = TITLE_PATTERN.match(line)
    if not match:
        return line, False
    sharps, title = match.group(1, 2)  # group 0 is the whole match.
    html_type = f"h{len(sharps)}"
    return html_node(html_type, trim(title)), True


def parse_all_bold(line: str) -> str:
    """Returns a string in which all occurences of bold markdown text are replaced by HTML bold."""
    return BOLD_PATTERN.sub(BOLD_REPLACEMENT, line)


def parse_all_emphasis(line: str) -> str:
    """Returns a string in which all occurences of emphasis markdown text are replaced by HTML em."""
    return EM_PATTERN.sub(EM_REPLACEMENT, line)


def parse_list_item(line: str, in_list: bool) -> Tuple[str, bool]:
    """Returns a list item <li>`text`</li> possibly surrounded by <ul> or </ul>
    depending on the `in_list` parameter."""
    match = LIST_PATTERN.match(line)
    if not match:
        if in_list:
            return f"{line}</ul>", True
        return line, False
    list_content = match.group(1)
    list_item = html_node("li", list_content)
    if not in_list:
        return f"<ul>{list_item}", True
    return list_item, True


# Just an helper function that should probably be elswhere (some other file)
def trim(string: str) -> str:
    """returns a string where surrounding spaces where removed."""
    return re.sub(r"^\s*|\s*$", "", string)
