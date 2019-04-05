"""Router."""
# routes = {
#     '/': 'Hello World',
#     '/goodbye': 'Goodbye World'
#     }
import os
import sys
import json
from vendor.mucca_logging.mucca_logging import logging
from src.client.client import client


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
            host = "localhost"
            port = 49153
            path = "/v1/sso/authentication"
            data = {"username": "admin@admin.moe", "password": "password"}
            method = "POST"
            my_client = client(host, port, path, json.dumps(data), method)
            response = my_client.client()
            logging.log_info(
                response,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            logging.log_info(
                "REQUEST {}".format(data),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            logging.log_info(
                "REQUEST {}".format(json.dumps(data)),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            logging.log_info(
                "METHOD {}".format(method),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            logging.log_info(
                "path {}".format(path),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            logging.log_info(
                "Host {} port {}".format(host, port),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            self.__getPort()
        else:
            logging.log_warning(
                'Bad request',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            pass

    def __login(self, request):
        """Login."""
        pass

    def __getPort(self):
        """Get port list."""
        path = '../muccapp/mucca_install/app/config/develop/config.json'
        dir_fd = os.open(path, os.O_RDONLY)
        # os.open(path, os.O_RDONLY, mode=0777)
        print("***************")
        print(os.open(path, os.O_RDONLY))
        # print("DIRFD {}".format(json.load(dir_fd)))
        pass
