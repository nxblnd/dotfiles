#!/usr/bin/env python3

from typing import Optional, Any


class Node:
    module: str
    key: str
    format: Optional[str]
    text: Optional[str]
    additional_entries: Optional[dict[str, type[Any]]]
    font_effect: Optional[str]
    neighbour_branches: str
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
        return str(self.construct_fastfetch_description())

    def construct_fastfetch_description(self) -> dict[str, str]:

        module = {"type": self.module}

        if self.font_effect:
            font_effect = self.font_effect
        else:
            font_effect = font_effects["reset"]
        key = {"key": f"{{{font_effect}}} {self.key}"}

        if self.format:
            format = {"format": self.format}
        else:
            format = {}

        if self.text:
            text = {"text": self.text}
        else:
            text = {}

        if self.additional_entries:
            additional_entries = self.additional_entries
        else:
            additional_entries = {}

        return module | key | format | text | additional_entries

    def add_children(self, *nodes: type["Node"]):
        self.children += nodes




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
)

modules["hardware_root"].add_children(
    modules["chassis"].add_children(
        modules["host"],
        modules["board"].add_children(modules["bios"]),
        modules["cpu"].add_children(modules["cpu_cache"]),
        modules["gpu"].add_children(modules["gpu_driver"]),
        modules["disk"],
        modules["ram"].add_children(modules["swap"]),
    ),
    modules["display"]
)

modules["misc_root"].add_children(
    modules["datetime"],
    modules["uptime"],
    modules["os_age"],
    modules["version"],
)
