import logging_helper
import middlewares
import transpara_logging
from transpara_logging import get_logger


print("hehe")
#region setup
@middlewares.log_middleware(suppress_exc=True)
def raise_suppressed():
    raise Exception("I was suppressed")

@middlewares.log_middleware(suppress_exc=True, suppressed_return_value=0)
def raise_suppressed_def():
    raise Exception("I was suppressed")
#endregion

#region tests
def test_suppress():
    assert raise_suppressed() == "I was suppressed"

def test_suppress_default():
    assert raise_suppressed_def() == 0
#endregion


transpara_logging.set_log_level(logging_helper.TRANSPARA_DEBUG_LEVEL)

get_logger(__name__).terror("t err")
get_logger(__name__).tdebug("tdebugging something")
get_logger(__name__).info("regular info")


test_suppress()
test_suppress_default()

transpara_logging.set_default_format("")
get_logger(__name__).info("regular info without format")

