from __future__ import annotations

import re

from rich import print
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text

GroupedDict = dict[str, list[str]]

RULE_URL = "https://www.flake8rules.com/rules/{}.html"


def group(lines: list[str]) -> GroupedDict:
    data: GroupedDict = {}
    for line in lines:
        match = re.search(r"\d+\:\d+\:\s(\w\d{3})", line)
        if match:
            code = match.group(1)
            if code not in data:
                data[code] = []
            data[code].append(line)
    data = {
        k: v
        for k, v in sorted(
            data.items(),
            key=lambda item: len(item[1]),
            reverse=True,
        )
    }
    return data


def dac_print(data: GroupedDict) -> None:
    total = 0

    for code, matches in data.items():
        # Print header
        head = Text(f"> {code} ({len(matches)}) ")
        head.stylize("bold red", 2, 6)
        link = Text(RULE_URL.format(code.upper()))
        link.stylize("dim", 0, 50)
        Console().rule(head + link, style="dim blue", align="left")

        # Print body
        errors = "\n".join([m for m in matches])
        panel = Panel.fit(errors, border_style="dim blue")
        pad = Padding(panel, (1, 4))
        print(pad)

        total += len(matches)
    print(f"Found {total} problems")
