import asyncio
from logging import getLogger
from pathlib import Path
from typing import Any, List

import orjson

from chew.utils import to_thread

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

    raise orjson.JSONDecodeError


def load_args(out_dir: Path) -> Any:
    return load_json(path=out_dir / ARGS_FILENAME)


def load_sota(out_dir: Path) -> Any:
    return load_json(path=out_dir / SOTA_FILENAME)


async def load(out_dir: Path):
    try:
        args = await to_thread(load_args, out_dir)
        sota = await to_thread(load_sota, out_dir)

        return {**args, 'path': out_dir / LOG_FILENAME}, sota
    except FileNotFoundError:
        return None


async def load_all(paths: List[Path]):
    futures = [
        load(out_dir)
        for path in paths for out_dir in path.iterdir()
        if out_dir.is_dir()
    ]
    data = await asyncio.gather(*futures)

    return zip(*[datum for datum in data if datum])
