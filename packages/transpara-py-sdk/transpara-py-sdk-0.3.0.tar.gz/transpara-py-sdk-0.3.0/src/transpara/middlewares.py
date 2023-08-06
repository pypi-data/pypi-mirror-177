from transpara.logging_config import Locals, GLOBAL_VERBOSE, TRANSPARA_DEBUG_LEVEL, TRANSPARA_ERROR_LEVEL

import os
import sys
import time
import logging
import traceback

import jsonpickle


exc_message = "RETURNEXCEPTION" #Used for returning the exception string when suppressing exceptions
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
def log_middleware(verbose_exc=False, suppress_exc=False, 
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
                logger.log(TRANSPARA_ERROR_LEVEL, f"{function.__name__}():{error_message}")

                #If measuring elapsed, log it before we bail
                if debug_elapsed:
                    debug_message = f"{function.__name__}():"
                    debug_message = f"{debug_message} elapsed: {(time.time() - start)*1000}ms"
                    logger.log(TRANSPARA_DEBUG_LEVEL, debug_message)     


                #If suppresing decide whether to return the exception message or an override value set as func param
                if suppress_exc: 
                    return error_message if suppressed_return_value == exc_message else suppressed_return_value

                #If exception wasn't suppresed above, then raise all chaos!
                raise
            
            if debug_locals or debug_elapsed: 

                #If there is anythign to debug (locals or elapsed) prepare message
                debug_message = f"{function.__name__}():"

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
        logger.log(TRANSPARA_DEBUG_LEVEL,f"{func.__name__}(): {message}")
        return result
    return wrapper