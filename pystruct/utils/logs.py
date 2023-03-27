import logging
import time
from functools import wraps

from pystruct.configs import VERBOSITY

import logging

#TODO redo the logs


class TechLogFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# create logger with 'spam_application'
tech_logger = logging.getLogger("My_app")
tech_logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(TechLogFormatter())
tech_logger.addHandler(ch)


# https://www.codegrepper.com/code-examples/python/python+print+error+in+red
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def log(*args, verbosity=1, rgb=(200, 200, 200)):
    if verbosity <= VERBOSITY:
        colored_args = tuple([colored(*rgb, arg) for arg in args])
        print(*colored_args)


def log_red(*args, **kwargs):
    log(*args, **kwargs, rgb=(200, 50, 50))


def log_pink(*args, **kwargs):
    log(*args, **kwargs, rgb=(255, 105, 180))


def log_yellow(*args, **kwargs):
    log(*args, **kwargs, rgb=(200, 200, 50))


def log_green(*args, **kwargs):
    log(*args, **kwargs, rgb=(50, 200, 50))


def log_cyan(*args, **kwargs):
    log(*args, **kwargs, rgb=(50, 200, 200))


#####################################################
def log_obj_stage(*args, **kwargs):
    log(*args, **kwargs)


def log_plantuml(*args, **kwargs):
    log_pink(*args, **kwargs)


def timing_log(_func):
    @wraps(_func)
    def wrapper(*args, **kwargs):
        tech_logger.info(f"[TIMING] Running {_func.__qualname__}...")

        start_time = time.time()
        res = _func(*args, **kwargs)
        elapsed_time = time.time()-start_time

        tech_logger.info(f"[TIMING] Function {_func.__qualname__} finished in {elapsed_time:2f} seconds.")
        return res
    return wrapper


def log_disk_ops(*args, **kwargs):
    log_pink(*args, **kwargs)



if __name__ == "__main__":
    log('test')
    log('test', rgb=(255, 0, 0))
    log('test', rgb=(0, 255, 0))
    log('test', rgb=(0, 0, 255))
    log('test', rgb=(0, 0, 0))
    log_red('red')
    log_yellow('yellow')
    log_cyan('cyan')
    log_green('green')

