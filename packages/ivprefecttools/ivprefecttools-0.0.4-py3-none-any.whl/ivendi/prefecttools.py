import os
import logging
from r7insight import R7InsightHandler
import functools

def r7_logging(func):
    @functools.wraps(func)
    def logging_wrapper(*args, **kwargs):
        extra_handlers = []

        r7Handler = None

        if not os.environ.get("RAPID7_TOKEN", None) == None:
            r7Handler = R7InsightHandler(os.environ["RAPID7_TOKEN"], "eu")
            extra_handlers.append(r7Handler)

        if len(extra_handlers) > 0:
            loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

            for logger in loggers:
                if logger.name.lower().startswith('prefect'):
                    for handler in extra_handlers:
                        logger.addHandler(handler)

        func(*args, **kwargs)

        if not r7Handler == None:
            r7Handler.flush()

    return logging_wrapper
