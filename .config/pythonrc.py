_auto_imports = [
    {"name": "sys", "module": "sys"},
    {"name": "os", "module": "os"},
    {"name": "Path", "module": "pathlib", "object": "Path"},
    {"name": "dt", "module": "datetime"},
    {"name": "collections", "module": "collections"},
    {"name": "pprint", "module": "pprint", "object": "pprint"},
    {"name": "it", "module": "itertools"},
    {"name": "tempfile", "module": "tempfile"},
    {"name": "subprocess", "module": "subprocess"},
    {"name": "json", "module": "json"},
]

def _autoimport():
    import importlib

    print('Auto importing libs:')

    for target in sorted(_auto_imports, key=lambda x: x["name"].lower()):
        try:
            module = importlib.import_module(target["module"])
        except Exception:
            continue

        obj = getattr(module, target["object"]) if target.get("object") else module
        globals()[target["name"]] = obj

        if target.get("object"):
            what = f'{target["object"]} from {target["module"]}'
        else:
            what = f'{target["module"]}'

        if target["module"] == target["name"]:
            named = ''
        else:
            named = f' as {target["name"]}'

        print(f'\t{what}{named}')

_autoimport()
