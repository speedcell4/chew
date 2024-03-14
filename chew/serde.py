import asyncio
from concurrent.futures import ThreadPoolExecutor
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

    raise orjson.JSONDecodeError


def load_args(out_dir: Path) -> Any:
    return load_json(path=out_dir / ARGS_FILENAME)


def load_sota(out_dir: Path) -> Any:
    return load_json(path=out_dir / SOTA_FILENAME)


def iter_dir(paths: List[Path]) -> List[Path]:
    for path in paths:
        for study_dir in path.iterdir():
            if study_dir.is_dir():
                yield study_dir


async def load(study_dir: Path, executor: ThreadPoolExecutor):
    try:
        loop = asyncio.get_running_loop()
        args = await loop.run_in_executor(executor, load_args, study_dir)
        sota = await loop.run_in_executor(executor, load_sota, study_dir)

        return {**args, 'path': study_dir / LOG_FILENAME}, sota
    except FileNotFoundError:
        return None


async def load_all(paths: List[Path]):
    with ThreadPoolExecutor() as executor:
        jobs = [load(path, executor=executor) for path in iter_dir(paths)]
        data = await asyncio.gather(*jobs)

    return zip(*[datum for datum in data if datum])
