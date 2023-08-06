# Copyright 2022 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import itertools
import re
import io
import textwrap
import typing as t

import pongo


class Frame(list):
    parent: t.Optional[list] = None


def parse_lines(f):
    key_value = re.compile(r"(\S+)\s*:\s*(\S.*)$")
    key_alone = re.compile(r"(\S+)\s*:\s*$")
    initframe = frame = Frame()
    current_indent = ""
    state: t.Literal["blockstart", "inlist", "instr"] = "inlist"

    def newframe(key):
        nonlocal frame
        newf = Frame()
        newf.parent = frame
        frame.append((key, newf))
        frame = newf

    def addpair(kv):
        frame.append(kv)

    def addstr(s):
        """
        Top frame isn't a list after all, it's a string
        """
        nonlocal frame
        assert len(frame) == 0
        frame = frame.parent
        key, _ = frame[-1]
        frame[-1] = (key, s)

    def appendstr(s):
        key, old = frame[-1]
        frame[-1] = (key, old + s)

    for ix, line in enumerate(f, 1):

        indent, remainder = re.match(r"^([ \t]*)(.*)$", line, re.S).groups()
        if line.strip().startswith("#") and state != "instr":
            continue
        if line.strip():
            if " " in indent and "\t" in indent:
                raise ValueError("Indentation mixes tabs and spaces")

            if state == "blockstart":
                if len(indent) <= len(current_indent):
                    # Not an indent after all, just an empty list item
                    state = "inlist"
                    addstr("")

                current_indent = indent

            elif state == "inlist":
                if len(indent) < len(current_indent):
                    frame = frame.parent
                    state = "inlist"

                elif len(indent) > len(current_indent):
                    raise ValueError(f"Unexpected indent at line {ix}: {line!r}")

                current_indent = indent

            elif state == "instr":
                if len(indent) < len(current_indent):
                    frame = frame.parent
                    state = "inlist"
                    current_indent = indent

        linenoprefix = line.removeprefix(current_indent)

        if state == "blockstart":
            if m := key_value.match(linenoprefix):
                addpair(m.groups())
                state = "inlist"
            elif m := key_alone.match(linenoprefix):
                newframe(m.group(1))
                state = "blockstart"
            elif linenoprefix.strip():
                addstr(linenoprefix)
                state = "instr"

        elif state == "inlist":
            if m := key_value.match(linenoprefix):
                addpair(m.groups())
                state = "inlist"
            elif m := key_alone.match(linenoprefix):
                newframe(m.group(1))
                state = "blockstart"
            elif line.strip():
                raise ValueError(f"Expected colon at line {ix}: {line!r}")

        elif state == "instr":
            appendstr(linenoprefix)
            state = "instr"

    return initframe


def test_parse_lines_handles_unexpected_indent():
    import pytest

    lines = ["a: a\n", "  b: b"]
    with pytest.raises(ValueError):
        assert parse_lines(lines)


def test_parse_lines_handles_unexpected_initial_indent():
    import pytest

    lines = ["  a: a\n"]
    with pytest.raises(ValueError):
        assert parse_lines(lines)


def test_parse_lines_handles_empty_items():
    import pytest

    lines = ["a:\n", "b:b"]
    assert parse_lines(lines) == [("a", ""), ("b", "b")]


def test_parse_lines_handles_multiline_strings():
    lines = [
        "a:\n",
        "  bbb\n",
        "\n",
        "  ccc\n",
    ]
    assert parse_lines(lines) == [("a", "bbb\n\nccc\n")]


def test_parse_lines_handles_indented_block():
    lines = ["a:\n", "  b:c"]
    assert parse_lines(lines) == [("a", [("b", "c")])]


def test_parse_lines_handles_nested_indented_block():
    lines = [
        "a:\n",
        "  b:\n",
        "    c: d\n",
        "    e: f\n",
    ]
    assert parse_lines(lines) == [("a", [("b", [("c", "d"), ("e", "f")])])]


def test_parse_lines():
    lines = [
        "a: b\n",
        "a: B\n",
        "c: \n",
        "  d: e\n",
        "  f: \n",
        "    ggg\n",
        "        hhh\n",
    ]
    assert parse_lines(lines) == [
        ("a", "b"),
        ("a", "B"),
        (
            "c",
            [
                ("d", "e"),
                ("f", "ggg\n    hhh\n"),
            ],
        ),
    ]


if __name__ == "__main__":
    main()
