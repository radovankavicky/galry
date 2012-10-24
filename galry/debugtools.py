import logging
import os.path
import traceback
import sys

__all__ = ['log_debug', 'log_info', 'log_warn',
           'debug_level', 'info_level', 'warning_level']

def setup_logging(level):
    if level == logging.DEBUG:
        logging.basicConfig(level=level,
                            format="%(asctime)s,%(msecs)03d  \
%(levelname)-7s  %(message)s",
                            datefmt='%H:%M:%S')
    else:
        logging.basicConfig(level=level,
                            # stream=sys.stdout,
                            format="%(levelname)-7s:  %(message)s")
    return logging.getLogger('galry')

def get_caller():
    tb = traceback.extract_stack()[-3]
    module = os.path.splitext(os.path.basename(tb[0]))[0].ljust(18)
    line = str(tb[1]).ljust(4)
    return "L:%s  %s" % (line, module)

    
# Logging methods
# ---------------
def log_debug(obj):
    if level == logging.DEBUG:
        string = str(obj)
        string = get_caller() + string
        logger.debug(string)
        
def log_info(obj):
    if level == logging.DEBUG:
        obj = get_caller() + str(obj)
    logger.info(obj)

def log_warn(obj):
    if level == logging.DEBUG:
        obj = get_caller() + str(obj)
    logger.warn(obj)

    
# Logging level methods
# ---------------------
def debug_level():
    logger.setLevel(logging.DEBUG)

def info_level():
    logger.setLevel(logging.INFO)

def warning_level():
    logger.setLevel(logging.WARNING)

# default level
# level = logging.DEBUG  # DEBUG
level = logging.WARNING
logger = setup_logging(level)


if __name__ == '__main__':
    log_debug("hello world")
    log_info("hello world")