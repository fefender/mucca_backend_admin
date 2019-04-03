"""Router."""
# routes = {
#     '/': 'Hello World',
#     '/goodbye': 'Goodbye World'
#     }
import os
import sys
from vendor.mucca_logging.mucca_logging import logging


class router():
    """Class router."""

    def __init__(self, path, request):
        """init."""
        self.path = path
        self.request = request
        self.paths = ['/login', '/logout']
        pass

    def rout(self):
        """Rout method."""
        if self.path in self.paths:
            logging.log_info(
                "{} is a valid path".format(self.path),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        else:
            logging.log_warning(
                'Bad request',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            pass
