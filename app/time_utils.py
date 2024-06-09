import time
import functools
import inspect

from loguru import logger


def log_exectuion_time(func):
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.opt(depth=1).info(
            f"Function {func.__name__} executed in {execution_time:.4f} seconds with {args, kwargs}"
        )
        return result

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.opt(depth=1).info(
            f"Function {func.__name__} executed in {execution_time:.4f} seconds with {args, kwargs}"
        )
        return result

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
