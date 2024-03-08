import functools
import logging
import sys

# root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# stdout handler
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_fn(fn):
    """
    decorator for logging the start and end of a function call
    """
    exclude_results = ["login"]         # functions to exclude when logging results (return values)
    exclude_keys = ["session_cookie"]   # kwargs keys to exclude from logging

    def get_log_value(value):
        """
        collapse collections into the collection length for logging purposes
        """
        if isinstance(value, list) or isinstance(value, dict):
            return f"{len(value)} items"
        return value

    def get_kwargs(**kwargs):
        """
        get filtered, condensed, formatted kwargs for logging
        """
        return [{k: get_log_value(v)} for k, v in kwargs.items() if k not in exclude_keys]

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        """
        inner portion of log_fn decorator
        """
        # log fn start
        start_msg = f"Starting execution of {fn.__name__} function"
        if fn.__name__ not in exclude_results:
            start_msg += f"kwargs: {get_kwargs(**kwargs)}"
        logger.info(start_msg)

        # call fn
        result = fn(*args, **kwargs)

        # log fn finish
        finish_msg = f"Finished execution of {fn.__name__} function"
        if fn.__name__ not in exclude_results:
            finish_msg += f" - result: {get_log_value(result)}"

        logger.info(finish_msg)
        return result

    return wrapper
