import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

ARGS_FILENAME = 'args.json'
SOTA_FILENAME = 'sota.json'


def load_json(path: Path) -> Any:
    with path.open(mode='r', encoding='utf-8') as fp:
        for _ in range(5):
            try:
                return json.load(fp=fp)
            except JSONDecodeError:
                pass

    raise JSONDecodeError


def load_args(out_dir: Path, name: str = ARGS_FILENAME) -> Any:
    return load_json(path=out_dir / name)


def load_sota(out_dir: Path, name: str = SOTA_FILENAME) -> Any:
    return load_json(path=out_dir / name)
