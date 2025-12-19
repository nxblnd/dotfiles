#!/usr/bin/env python3

from typing import Optional, Any, Iterator
import json
from tempfile import NamedTemporaryFile
import subprocess
from pathlib import Path


def flatten(obj) -> Iterator[Any]:
    for value in obj:
        if isinstance(value, list):
            yield from flatten(value)
        else:
            yield value


class Node:
    module: str
    key: str
    format: Optional[str]
    text: Optional[str]
    additional_entries: Optional[dict[str, type[Any]]]
    font_effect: Optional[str]
    children: list["Node"]

    def __init__(self, module, key, format=None, additional_entries=None, text=None, font_effect=None):
        self.module = module
        self.key = key
        self.format = format
        self.text = text
        self.additional_entries = additional_entries
        self.font_effect = font_effect
        self.children = []

    def __str__(self) -> str:
        return f'Node {self.construct_module()}, children: {self.children}'

    def __repr__(self) -> str:
        return self.__str__()

    def construct_module(self) -> dict[str, type[Any]]:

        module = {"type": self.module}
        key = {"key": self.key}
        format = {"format": self.format} if self.format else {}
        text = {"text": self.text} if self.text else {}
        additional_entries = self.additional_entries if self.additional_entries else {}

        return module | key | format | text | additional_entries

    def collect_branch(self) -> list[dict]:
        return [self.construct_module()] + [node.collect_branch() for node in self.children]

    def add_children(self, *nodes: type["Node"]) -> type["Node"]:
        self.children += nodes
        return self

    def remove_module(self, module) -> None:
        for i, node in enumerate(self.children):
            if node.module == module:
                del self.children[i]
                return
            node.remove_module(module)

    def prettify(self, font_effect="", key_prefix="") -> None:
        if self.font_effect:
            font_effect = self.font_effect
            self.key = font_effect + self.key

        if len(key_prefix):
            self.key = key_prefix + f'{graphics["hbar"]} ' + self.key

            if key_prefix[-1] == graphics["end"]:
                key_prefix = key_prefix[:-1] + '   '
            else:
                key_prefix = key_prefix[:-1] + graphics["vbar"] + '  '

        for i, node in enumerate(self.children):
            if i == len(self.children) - 1:
                node.prettify(font_effect, key_prefix + font_effect + graphics["end"])
            else:
                node.prettify(font_effect, key_prefix + font_effect + graphics["branch"])


font_effects = {
    "reset": "{#0}",
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
    "bootmgr": Node("bootmgr", "Boot", format="{name}"),
    "init": Node("initsystem", "Init"),
    "kernel": Node("kernel", "Kernel"),
    "lm": Node("lm", "LM"),
    "packages": Node("packages", "Packages"),
    "terminal": Node("terminal", "Terminal", font_effect=font_effects["terminal"]),
    "terminal_font": Node("terminalfont", "Font"),
    "shell": Node("shell", "Shell"),
    "graphics": Node("custom", "Graphics", font_effect=font_effects["graphics"]),
    "de": Node("de", "DE"),
    "wm": Node("wm", "WM"),
    "icons": Node("icons", "Icons"),
    "cursor": Node("cursor", "Cursor"),
    "font": Node("font", "Font"),
    "theme": Node("theme", "Theme"),
    "development": Node("custom", "Development", font_effect=font_effects["development"]),
    "editor": Node("editor", "Editor"),
    "git": Node("command", "Git", text="git --version", format="{~12}"),
    "python": Node("command", "Python", text="python --version", format="{~7}"),
    "gcc": Node("command", "GCC", text="gcc --version | head -1 | cut -d ' ' -f 3", format="{}"),
    "clang": Node("command", "Clang", text="clang --version | head -1 | cut -d ' ' -f 3", format="{}"),
    "nodejs": Node("command", "NodeJS", text="node --version", format="{}"),
    "hardware_root": Node("custom", "Hardware", font_effect=font_effects["hardware"]),
    "chassis": Node("chassis", "Chassis"),
    "host": Node("host", "Host", format="{vendor} {name}"),
    "board": Node("board", "Board"),
    "bios": Node("bios", "BIOS", format="[{type}] {vendor} {version}"),
    "cpu": Node("cpu", "CPU"),
    "cpu_cache": Node("cpucache", "CPU Cache"),
    "gpu": Node("gpu", "GPU", format="[{type}] {vendor} {name}"),
    "gpu_driver": Node("gpu", "Driver", format="{driver}"),
    "disk": Node("disk", "Disk"),
    "ram": Node("memory", "RAM"),
    "swap": Node("swap", "Swap"),
    "battery": Node("battery", "Battery"),
    "display": Node("display", "Display"),
    "misc_root": Node("custom", "Miscellaneous information", font_effect=font_effects["miscellaneous"]),
    "datetime": Node("datetime", "Date & Time"),
    "uptime": Node("uptime", "Uptime"),
    "os_age": Node("disk", "OS age", format="{days} days (since {create-time:10})", additional_entries={"folders": "/"}),
    "media": Node("media", "Now playing"),
    "version": Node("version", "Fastfetch", format="{version}"),
}

roots = [
    modules["software_root"].add_children(
        modules["os"].add_children(
            modules["bootmgr"],
            modules["init"],
            modules["kernel"],
            modules["lm"],
            modules["packages"],
        ),
        modules["terminal"].add_children(
            modules["shell"],
            modules["terminal_font"],
        ),
        modules["graphics"].add_children(
            modules["de"],
            modules["wm"],
            modules["icons"],
            modules["cursor"],
            modules["font"],
            modules["theme"],
        ),
        modules["development"].add_children(
            modules["editor"],
            modules["git"],
            modules["python"],
            modules["gcc"],
            modules["clang"],
            modules["nodejs"],
        ),
    ),
    modules["hardware_root"].add_children(
        modules["chassis"].add_children(
            modules["host"],
            modules["board"].add_children(modules["bios"]),
            modules["cpu"].add_children(modules["cpu_cache"]),
            modules["gpu"].add_children(modules["gpu_driver"]),
            modules["disk"],
            modules["ram"].add_children(modules["swap"]),
            modules["battery"],
        ),
        modules["display"]
    ),
    modules["misc_root"].add_children(
        modules["datetime"],
        modules["uptime"],
        modules["os_age"],
        modules["version"],
    )
]


def build_config(roots: list[Node]) -> dict[str, type[Any]]:
    schema = {
        "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json"
    }

    logo = {"padding": {"left": 3, "right": 3, "top": 3}}

    modules = {"modules": list(flatten(root.collect_branch() for root in roots))}

    return schema | logo | modules


def get_test_response(config: dict[str, type[Any]]) -> list[dict]:
    with NamedTemporaryFile(mode='w', delete_on_close=False, suffix=".jsonc") as tmp_config:
        json.dump(config, tmp_config)
        tmp_config.flush()

        fastfetch_response = subprocess.run(
            ["fastfetch", "--config", tmp_config.name, "--json"],
            capture_output=True
        )

    return json.loads(fastfetch_response.stdout)


def filter_roots(roots: list[Node], data: list[dict]) -> list[Node]:
    skip_modules = ["Custom"]
    for response_object in data:
        if response_object.get("error") and response_object.get("type") not in skip_modules or response_object.get("result") == []:
            for root in roots:
                root.remove_module(response_object.get("type").lower())
    return roots


def main():
    test_config = build_config(roots)
    test_data = get_test_response(test_config)
    filtered_roots = filter_roots(roots, test_data)
    for root in filtered_roots:
        root.prettify()
    final_config = build_config(filtered_roots)
    fastfetch_config = Path.home() / ".config" / "fastfetch" / "config_generated.jsonc"
    with open(fastfetch_config, 'w') as config_file:
        json.dump(final_config, config_file)


if __name__ == '__main__':
    main()
