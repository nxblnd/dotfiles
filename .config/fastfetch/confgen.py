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

    def __init__(
        self,
        module,
        key,
        format=None,
        additional_entries=None,
        text=None,
        font_effect=None,
    ):
        self.module = module
        self.key = key
        self.format = format
        self.text = text
        self.additional_entries = additional_entries
        self.font_effect = font_effect
        self.children = []

    def __str__(self) -> str:
        return f"Node {self.construct_module()}, children: {self.children}"

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
        return [self.construct_module()] + [
            node.collect_branch() for node in self.children
        ]

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

            # bold for category roots
            self.key = font_effect + BOLD_CODE + self.key

        if len(key_prefix):
            self.key = key_prefix + f'{graphics["hbar"]} ' + self.key

            if key_prefix[-1] == graphics["end"]:
                key_prefix = key_prefix[:-1] + "   "
            else:
                key_prefix = key_prefix[:-1] + graphics["vbar"] + "  "

        for i, node in enumerate(self.children):
            if i == len(self.children) - 1:
                node.prettify(font_effect, key_prefix + font_effect + graphics["end"])
            else:
                node.prettify(
                    font_effect, key_prefix + font_effect + graphics["branch"]
                )


CSI = "\033["
SGR = "m"
BOLD = 1
BOLD_CODE = f"{CSI}{BOLD}{SGR}"


def fg(r, g, b):
    FORE = 38
    TRUE_COLOR = 2
    THIN_COLOR = 22
    thin_code = f"{CSI}{THIN_COLOR}{SGR}"
    return f"{thin_code}{CSI}{FORE};{TRUE_COLOR};{r};{g};{b}{SGR}"


font_effects = {
    "reset": f"{CSI}{SGR}",
    "software": fg(0, 255, 0),
    "os": fg(0, 255, 60),
    "terminal": fg(0, 255, 120),
    "graphics": fg(0, 255, 180),
    "development": fg(0, 255, 240),
    "hardware": fg(255, 255, 0),
    "chassis": fg(255, 180, 0),
    "network": fg(0, 150, 255),
    "miscellaneous": fg(195, 120, 225),
}

graphics = {
    "branch": "├",
    "vbar": "│",
    "end": "└",
    "hbar": "─",
}

modules = {
    "software_root": Node("custom", "Software", font_effect=font_effects["software"]),
    "os": Node("os", "OS", font_effect=font_effects["os"]),
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
    "development": Node(
        "custom", "Development", font_effect=font_effects["development"]
    ),
    "editor": Node("editor", "Editor"),
    "git": Node("command", "Git", text="git --version", format="{~12}"),
    "python": Node("command", "Python", text="python --version", format="{~7}"),
    "gcc": Node(
        "command", "GCC", text="gcc --version | head -1 | cut -d ' ' -f 3", format="{}"
    ),
    "clang": Node(
        "command",
        "Clang",
        text="clang --version | head -1 | cut -d ' ' -f 3",
        format="{}",
    ),
    "nodejs": Node("command", "NodeJS", text="node --version", format="{}"),
    "hardware_root": Node("custom", "Hardware", font_effect=font_effects["hardware"]),
    "chassis": Node("chassis", "Chassis", font_effect=font_effects["chassis"]),
    "host": Node("host", "Host", format="{vendor} {name}"),
    "board": Node("board", "Board"),
    "bios": Node("bios", "BIOS", format="[{type}] {vendor} {version}"),
    "cpu": Node("cpu", "CPU"),
    "cpu_cache": Node("cpucache", "CPU Cache", format="{result}"),
    "gpu": Node("gpu", "GPU", format="[{type}] {vendor} {name}"),
    "gpu_driver": Node("gpu", "Driver", format="{driver}"),
    "disk": Node("disk", "Disk"),
    "ram": Node("memory", "RAM"),
    "swap": Node("swap", "Swap"),
    "battery": Node("battery", "Battery"),
    "power_adapter": Node("poweradapter", "Power Adapter"),
    "display": Node("display", "Display"),
    "input_devices": Node("custom", "Input devices"),
    "keyboard": Node("keyboard", "Keyboard"),
    "mouse": Node("mouse", "Mouse"),
    "gamepad": Node("gamepad", "Gamepad"),
    "misc_root": Node(
        "custom", "Miscellaneous information", font_effect=font_effects["miscellaneous"]
    ),
    "datetime": Node("datetime", "Date & Time"),
    "browser": Node(
        "command",
        "Browser",
        text="eval $( \
            cat /usr/share/applications/$(xdg-mime query default text/html) | \
            grep -Eo 'Exec=([A-Za-z\\/]+)' | \
            head -1 | cut -c 6- | { cat | tr -d '\n'; echo ' --version'; })",
    ),
    "uptime": Node("uptime", "Uptime"),
    "os_age": Node(
        "disk",
        "OS age",
        format="{days} days (since {create-time:10})",
        additional_entries={"folders": "/"},
    ),
    "media": Node("media", "Now playing"),
    "version": Node("version", "Fastfetch", format="{version}"),
    "network_root": Node("custom", "Networks", font_effect=font_effects["network"]),
    "bluetooth": Node("bluetoothradio", "Bluetooth"),
    "dns": Node("dns", "DNS"),
    "local_ip": Node("localIp", "Local IP"),
    "public_ip": Node("publicIp", "Public IP"),
    "wifi": Node("wifi", "Wi-Fi"),
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
            modules["cpu"],
            modules["gpu"].add_children(modules["gpu_driver"]),
            modules["disk"],
            modules["ram"].add_children(modules["swap"]),
            modules["battery"].add_children(modules["power_adapter"]),
        ),
        modules["display"],
        modules["input_devices"].add_children(
            modules["keyboard"],
            modules["mouse"],
            modules["gamepad"],
        ),
    ),
    modules["network_root"].add_children(
        modules["bluetooth"],
        modules["dns"],
        modules["local_ip"],
        # modules["public_ip"],
        modules["wifi"],
    ),
    modules["misc_root"].add_children(
        modules["browser"],
        modules["datetime"],
        modules["uptime"],
        modules["os_age"],
        modules["version"],
    ),
]


def build_config(roots: list[Node]) -> dict[str, type[Any]]:
    schema = {
        "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json"
    }

    logo = {"padding": {"left": 3, "right": 3, "top": 3}}

    modules = {"modules": list(flatten(root.collect_branch() for root in roots))}

    return schema | logo | modules


def get_test_response(config: dict[str, type[Any]]) -> list[dict]:
    with NamedTemporaryFile(
        mode="w", delete_on_close=False, suffix=".jsonc"
    ) as tmp_config:
        json.dump(config, tmp_config)
        tmp_config.flush()

        fastfetch_response = subprocess.run(
            ["fastfetch", "--config", tmp_config.name, "--json"], capture_output=True
        )

    return json.loads(fastfetch_response.stdout)


def filter_roots(roots: list[Node], data: list[dict]) -> list[Node]:
    skip_modules = ["Custom"]
    for response_object in data:
        if (
            response_object.get("error")
            and response_object.get("type") not in skip_modules
            or response_object.get("result") == []
        ):
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
    with open(fastfetch_config, "w") as config_file:
        json.dump(final_config, config_file, indent=2)


if __name__ == "__main__":
    main()
