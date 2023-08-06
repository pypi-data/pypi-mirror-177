from unittest.case import TestCase
import logging
from ds4biz_commons.business.decorators import FunctionLogger

class DecoratorsTest(TestCase):
    def test_function_logging(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig()
        logger.setLevel(logging.DEBUG)
        
        @FunctionLogger(logger.debug)
        def f(a,b):
            return a+b
        f(1,3)
