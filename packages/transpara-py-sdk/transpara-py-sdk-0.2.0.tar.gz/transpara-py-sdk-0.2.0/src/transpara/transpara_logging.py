import logging
from logging import Logger
from transpara.logging_helper import GLOBAL_VERBOSE, TRANSPARA_DEBUG_LEVEL, TRANSPARA_ERROR_LEVEL, init_logger
from transpara import logging_helper

class TransparaLogger(Logger):
    
    def terror(self, msg):
        self.log(TRANSPARA_ERROR_LEVEL, msg)

    def tdebug(self, msg):
        self.log(TRANSPARA_DEBUG_LEVEL, msg)

#Monkeypatching the class as I don't want to lose information by calling the logger from an interim function
Logger.terror = TransparaLogger.terror
Logger.tdebug = TransparaLogger.tdebug

def get_logger(logger_name) -> TransparaLogger:
    return logging.getLogger(logger_name)

def set_log_level(level:int):
    logging.root.setLevel(level)

"""
Sets verbose exception stacks
"""
def set_global_verbose(val:bool):
    global GLOBAL_VERBOSE
    GLOBAL_VERBOSE = val

def set_default_format(fmt:str):
    logging_helper.default_format = fmt
    init_logger()

def set_tdebug_format(fmt:str):
    logging_helper.debug_handler_format = fmt
    init_logger()

def set_terror_format(fmt:str):
    logging_helper.error_handler_format = fmt 
    init_logger()
