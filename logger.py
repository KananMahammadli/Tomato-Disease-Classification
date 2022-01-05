import logging
import sys


APP_LOGGER_NAME = 'tomato-disease-classification'
def setup_applevel_logger(logger_name = APP_LOGGER_NAME, file_name='app_debug.log'): 
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)
    if file_name:
        fh = logging.FileHandler(file_name, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

def get_logger(module_name):    
   return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)