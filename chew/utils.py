import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

thread_executor = ThreadPoolExecutor()
process_executor = ProcessPoolExecutor()


def to_thread(fn, *args):
    return asyncio.get_running_loop().run_in_executor(thread_executor, fn, *args)


def to_process(fn, *args):
    return asyncio.get_running_loop().run_in_executor(process_executor, fn, *args)
