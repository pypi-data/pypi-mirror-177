
"""
ERROR = 60 >> ADDED BY ARTURO
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
"""
import logging
import sys
import traceback as tb

GLOBAL_VERBOSE = False #settings.LOG_GLOBAL_VERBOSE

def set_global_verbose(val:bool):
    global GLOBAL_VERBOSE
    GLOBAL_VERBOSE = val

#Need a custom logging level for custom formats on error handler
NEW_ERROR_LEVEL = 60
logging.addLevelName(NEW_ERROR_LEVEL, "ERROR")
#Probs want a delimiter? like >> << If we ever want to parse our logs it would be useful to have some sort of delimiter
default_format = ">> [%(levelname)s: %(asctime)s: %(name)s: %(filename)s:%(lineno)s - %(funcName)5s()]: %(message)s <<"

#the decorator cant use filename and fileno or it would use the own decorator, so what we do is we get the function name from the decorator and pass that
#we don't have the line number in this case but that's ok
decorator_error_handler_format = ">> [%(levelname)s: %(asctime)s: %(name)s: %(message)s <<"

#custom formatter based on log level
class TransparaCustomLogFormatter(logging.Formatter):

    def __init__(self):
        super().__init__(fmt=default_format,
         datefmt=None, 
         style='%')  
    
    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == NEW_ERROR_LEVEL:
            self._style._fmt = decorator_error_handler_format

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig
        return result

#configure logger with formatter 
formatter = TransparaCustomLogFormatter()
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logging.root.addHandler(stream_handler)


#Used for returning the exception string when suppressing exceptions
RETURN_EXCEPTION = "RETURNEXCEPTION"

"""
Examples:
@handle_err()
@handle_err(supress=True)
@handle_err(False, True, "")
@handle_err(False, True, "", True)
"""
def handle_err(verbose=False, supress=False, default_supress_value = RETURN_EXCEPTION, single_line = False, single_line_separator = "||"):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
            except BaseException as e:
                logger = logging.getLogger(function.__module__)
                error_message = str(e)

                if verbose or GLOBAL_VERBOSE:
                    error_message = tb.format_exc()

                error_message = error_message if not single_line else single_line_separator.join(l for l in error_message.splitlines() if l)
                logger.log(NEW_ERROR_LEVEL, f"{function.__name__}()]:{error_message}")
                if supress:
                    if default_supress_value == RETURN_EXCEPTION:
                        return error_message
                    return default_supress_value
                raise
            return result
        return wrapper
    return decorator