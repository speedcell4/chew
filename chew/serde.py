import json
from logging import getLogger
from pathlib import Path
from typing import Any, List

import orjson

logger = getLogger(__name__)

LOG_FILENAME = 'log.txt'
ARGS_FILENAME = 'args.json'
SOTA_FILENAME = 'sota.json'


def load_json(path: Path) -> Any:
    with path.open(mode='r', encoding='utf-8') as fp:
        for _ in range(5):
            try:
                return orjson.loads(fp.read())
            except orjson.JSONDecodeError:
                pass

        try:
            return json.load(fp)
        except json.JSONDecodeError:
            pass

    raise ValueError(f'{path} is not a valid JSON')


def load_args(out_dir: Path) -> Any:
    return load_json(path=out_dir / ARGS_FILENAME)


def load_sota(out_dir: Path) -> Any:
    return load_json(path=out_dir / SOTA_FILENAME)


def load(out_dir: Path):
    args = load_args(out_dir)
    sota = load_sota(out_dir)

    return {**args, 'path': out_dir / LOG_FILENAME}, sota


def load_all(paths: List[Path]):
    args, sota = [], []

    for path in paths:
        for out_dir in path.iterdir():
            if out_dir.is_dir():
                try:
                    a, s = load(out_dir)
                    args.append(a)
                    sota.append(s)
                except (ValueError, FileNotFoundError):
                    pass

    return args, sota
