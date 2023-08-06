import os
import logging
import functools
from enum import Enum
from r7insight import R7InsightHandler


def ivendi_flow(environment_variables: Enum):
        def logging_wrapper(func):
            r7Handler = None
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                extra_handlers = []
                validate_environment(environment_variables)

                if not os.environ.get("RAPID7_TOKEN", None) == None:
                    r7Handler = R7InsightHandler(os.environ["RAPID7_TOKEN"], "eu")
                    extra_handlers.append(r7Handler)

                if len(extra_handlers) > 0:
                    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

                    for logger in loggers:
                        if logger.name.lower().startswith('prefect'):
                            for handler in extra_handlers:
                                logger.addHandler(handler)

                retval = func(*args, **kwargs)

                if not r7Handler == None:
                    r7Handler.flush()

                return retval
            return wrapper
        return logging_wrapper


def validate_environment(env_vars):

    missing_env_vars = []
    for env_var in env_vars:
        if (os.environ.get(env_var.name, None) == None):
            missing_env_vars.append(env_var.name)

    if (len(missing_env_vars) > 0):
        raise Exception(f'Required env vars not set: {missing_env_vars}')