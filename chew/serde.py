import json
from pathlib import Path
from typing import Any


def load_json(path: Path, default: Any = None) -> Any:
    try:
        with path.open(mode='r', encoding='utf-8') as fp:
            return json.load(fp=fp)
    except FileNotFoundError as error:
        if default is not None:
            return default
        raise error


ARGS_FILENAME = 'args.json'
SOTA_FILENAME = 'sota.json'


def load_args(out_dir: Path, name: str = ARGS_FILENAME) -> Any:
    return load_json(path=out_dir / name)


def load_sota(out_dir: Path, name: str = SOTA_FILENAME) -> Any:
    return load_json(path=out_dir / name)
