#!/usr/bin/env python3

from typing import Optional


class Node:
    module: str
    key: str
    format: Optional[str]
    text: Optional[str]
    font_effect: Optional[str]
    neighbour_branches: str
    children: list["Node"] = []

    def __init__(self, module, key, format=None, text=None, font_effect=None):
        self.module = module
        self.key = key
        self.format = format
        self.text = text
        self.font_effect = font_effect

    def __str__(self) -> str:
        return str(self.construct_fastfetch_description())

    def construct_fastfetch_description(self) -> dict[str, str]:

        module = {"type": self.module}

        if self.font_effect:
            font_effect = self.font_effect
        else:
            font_effect = font_effects["reset"]
        key = {"key": f"{{{font_effect}}} {self.key}"}

        if self.format:
            format = self.format
        else:
            format = {}

        if self.text:
            text = self.text
        else:
            text = {}

        return module | key | format | text

    def add_children(self, *nodes: type["Node"]):
        for node in nodes:
            self.children.append(node)


schema = {
    "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json"
}

logo = {"padding": {"left": 3, "right": 3, "top": 3}}

font_effects = {
    "reset": "#0",
    "software": "\u001b[38;2;0;255;0m",
    "os": "\u001b[38;2;0;255;60m",
    "terminal": "\u001b[38;2;0;255;120m",
    "graphics": "\u001b[38;2;0;255;180m",
    "development": "\u001b[38;2;0;255;240m",
    "hardware": "\u001b[38;2;255;255;0m",
    "chassis": "\u001b[38;2;255;180;0m",
    "miscellaneous": "\u001b[38;2;195;120;225m",
}

graphics = {
    "branch": "├",
    "vbar": "│",
    "end": "└",
    "hbar": "─",
}

modules = {
    "software_root": Node("custom", "Software", font_effect=font_effects["software"]),
    "os": Node("os", "OS"),
}

modules["software_root"].add_children(modules["os"])

print(modules["software_root"])
