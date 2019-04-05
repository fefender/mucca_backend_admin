"""HTTP Client."""
import os
import sys
from vendor.mucca_logging.mucca_logging import logging
import http.client


class client():
    """http client class."""

    def __init__(self, host, port, url, data, method):
        """Init."""
        self.host = host
        self.port = port
        self.url = url
        self.data = data
        self.method = method
        self.source = os.getenv("SERVER_HOST") + ":" + os.getenv("SERVER_PORT")

    def client(self):
        """Client."""
        print("*****BEFORE http connection")
        client = http.client.HTTPConnection(self.host, self.port)
        print("*****http connection client {}".format(client))
        # body = "body"
        headers = {'Content-Type': 'application/json'}
        # chunked = False
        client.request(self.method, self.url, self.data, headers)
        response = client.getresponse()
        print(dir(response))
        logging.log_info(
            "Client response in client {}".format(response.read()),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return response
    pass
