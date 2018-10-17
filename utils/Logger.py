import logging
import traceback
from .Colorizer import Colorizer

logger = logging.getLogger(__name__)

class Logger:

    @classmethod
    def log(cls, string):
        logger.log(string)

    @classmethod
    def error(cls, exception):
        logger.error(Colorizer.Red(exception))
        logger.error(' ')
        logger.error(Colorizer.Yellow('EXCEPTION'))
        logger.error(' ')
        logger.error(Colorizer.Yellow(cls.stack(exception)))

    @classmethod
    def stack(cls, excp):
        stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)
        pretty = traceback.format_list(stack)
        return ''.join(pretty) + '\n  {} {}'.format(excp.__class__, excp)

    @classmethod
    def stack_list(cls, excp):
        stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)
        pretty = traceback.format_list(stack)
        return ''.join(pretty) + '\n  {} {}'.format(excp.__class__, excp)

