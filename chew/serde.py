import json
from json import JSONDecodeError
from logging import getLogger
from pathlib import Path
from typing import Any, List

logger = getLogger(__name__)

LOG_FILENAME = 'log.txt'
ARGS_FILENAME = 'args.json'
SOTA_FILENAME = 'sota.json'


def load_json(path: Path, num_retries: int = 5) -> Any:
    with path.open(mode='r', encoding='utf-8') as fp:
        for _ in range(num_retries):
            try:
                return json.load(fp)
            except JSONDecodeError:
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
