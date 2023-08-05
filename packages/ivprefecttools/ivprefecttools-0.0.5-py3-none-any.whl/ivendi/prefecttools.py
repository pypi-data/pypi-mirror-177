import os
import logging
from r7insight import R7InsightHandler
import functools
from prefect import task, get_run_logger

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

@task
def validate_environment(env_vars):
    logger = get_run_logger()
    logger.info("validating environment")

    missing_env_vars = []
    for env_var in env_vars:
        if (os.environ.get(env_var.name, None) == None):
            missing_env_vars.append(env_var.name)

    if (len(missing_env_vars) > 0):
        raise Exception(f'Required env vars not set: {missing_env_vars}')
    else:
        logger.info("validated environment")