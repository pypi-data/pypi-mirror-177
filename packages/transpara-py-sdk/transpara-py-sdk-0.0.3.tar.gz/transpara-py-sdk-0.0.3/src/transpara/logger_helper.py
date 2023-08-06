"""
ERROR = 60 >> ADDED BY ARTURO
TRANSPARA_DEBUG = 15 >> ADDED BY ARTURO
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
"""
import logging
import os
import sys
import time
import traceback

import jsonpickle

#Need a custom logging level for custom formats on error handler
TRANSPARA_ERROR_LEVEL = 60
TRANSPARA_DEBUG_LEVEL = 15
logging.addLevelName(TRANSPARA_ERROR_LEVEL, "TERROR")
logging.addLevelName(TRANSPARA_DEBUG_LEVEL, "TDEBUG")
#Probs want a delimiter? like >> << If we ever want to parse our logs it would be useful to have some sort of delimiter
default_format = ">> [%(levelname)s: %(asctime)s: %(name)s: %(filename)s:%(lineno)s - %(funcName)5s()]: %(message)s <<"


grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
blue = "\x1b[34;20m"
bold_red = "\x1b[31;1m"
reset_color = "\x1b[0m"

#the decorator cant use filename and fileno or it would use the own decorator, so what we do is we get the function name from the decorator and pass that
#we don't have the line number in this case but that's ok
decorator_error_handler_format = f">> {red}[%(levelname)s: %(asctime)s: %(name)s: %(message)s <<"
decorator_debug_handler_format = f">> {blue}[%(levelname)s: %(asctime)s: %(name)s: %(message)s <<"

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
        if record.levelno == TRANSPARA_ERROR_LEVEL:
            self._style._fmt = decorator_error_handler_format

        if record.levelno == TRANSPARA_DEBUG_LEVEL:
            self._style._fmt = decorator_debug_handler_format

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

#Ideally this would be set upong settings initialization #settings.LOG_GLOBAL_VERBOSE
GLOBAL_VERBOSE = False 

def set_log_level(level:int):
    logging.root.setLevel(level)

def set_global_verbose(val:bool):
    global GLOBAL_VERBOSE
    GLOBAL_VERBOSE = val


#Used for returning the exception string when suppressing exceptions
exc_message = "RETURNEXCEPTION"


class Locals():

    def any(self):
        return len(self.__dict_) > 0

    def set(self, locals_dict):
        self.__dict__ = locals_dict

    def to_json(self):
        return jsonpickle.encode(self.__dict__)


"""
    [OPTIONAL][Default False] verbose_exc              if true, logs the stack trace, else just log the exception message
    [OPTIONAL][Default False] suppress_exc             will surround the exception and won't rethrow it by default it will return the error message to the caller
    [OPTIONAL][Default False] suppressed_return_value  If suppressing the exception, by default the function will return the error message unless this argument is set
    [OPTIONAL][Default False] log_locals_on_exc        if true, the locals of the called function will be logged when there is an exception
    [OPTIONAL][Default False] debug_locals             if true, the locals of the called function will be logged when there are no exceptions
    [OPTIONAL][Default True] debug_elapsed            by default regardless of exception conditions, the elapsed time of the called function will be logged

    @transpara_middleware(suppress_exc=True, log_locals_on_exc=True, debug_elapsed=True)
    @transpara_middleware()
"""
def transpara_middleware(verbose_exc=False, suppress_exc=False, 
                suppressed_return_value = exc_message,
                log_locals_on_exc=False, 
                debug_locals = False,
                debug_elapsed = True
            ):

    def decorator(function):
        def wrapper(*args, **kwargs):

            if debug_elapsed:
                start = time.time()


            #Get a logger
            logger = logging.getLogger(function.__module__)

            #If debugging locals then set a tracer to get the locals
            #From the stack frame
            if debug_locals:
                locals = Locals()
                def tracer(frame, event, arg):
                    if event=='return':
                        locals.set(frame.f_locals.copy())

            try:
                #set local tracer
                if debug_locals: sys.setprofile(tracer)
                #invoke actual function
                result = function(*args, **kwargs)
                #Set back original tracer
                if debug_locals: sys.setprofile(None)        
            except BaseException as e:
                #Set back original tracer
                if debug_locals: sys.setprofile(None)

                error_message = str(e)

                #If exceptions are set to verbose then print the stack trace 
                if verbose_exc or GLOBAL_VERBOSE:
                    error_message = traceback.format_exc()

                #Capture locals from stack and add them to the error message
                if log_locals_on_exc:
                    try:
                        tb = sys.exc_info()[2]
                        locals_dict = tb.tb_next.tb_frame.f_locals
                        locals_json = jsonpickle.encode(locals_dict)
                        error_message = error_message + os.linesep + "locals: "+ locals_json
                    except:
                        pass

                #Log the error
                logger.log(TRANSPARA_ERROR_LEVEL, f"{function.__name__}()]{reset_color}:{error_message}")

                #If measuring elapsed, log it before we bail
                if debug_elapsed:
                    debug_message = f"{function.__name__}(){reset_color}]:"
                    debug_message = f"{debug_message} elapsed: {(time.time() - start)*1000}ms"
                    logger.log(TRANSPARA_DEBUG_LEVEL, debug_message)     


                #If suppresing decide whether to return the exception message or an override value set as func param
                if suppress_exc: 
                    return error_message if suppressed_return_value == exc_message else suppressed_return_value

                #If exception wasn't suppresed above, then raise all chaos!
                raise
            
            if debug_locals or debug_elapsed: 

                #If there is anythign to debug (locals or elapsed) prepare message
                debug_message = f"{function.__name__}(){reset_color}]:"

                #if measuring executing time, add to debug message
                if debug_elapsed: debug_message = f"{debug_message} elapsed: {(time.time() - start)*1000}ms"

                #if debugging the locals, add them to the message
                if debug_locals and locals.any: debug_message = f"{debug_message} locals: {locals.to_json()}"

                #log the debug message
                logger.log(TRANSPARA_DEBUG_LEVEL, debug_message)     


            return result
        return wrapper
    return decorator


def debug_elapsed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        logger = logging.getLogger(func.__module__)
        result = func(*args, **kwargs)
        message = f"Elapsed: {(time.time() - start)*1000}ms"
        logger.log(TRANSPARA_DEBUG_LEVEL,f"{func.__name__}(){reset_color}]: {message}")
        return result
    return wrapper
