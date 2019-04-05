"""Mucca Back End Admin."""

import socketserver
import http.server
from dotenv import load_dotenv
from dotenv import find_dotenv
import os
import sys
from src.server.server import RequestHandler
from vendor.mucca_logging.mucca_logging import logging


class app():
    """App."""

    def __init__(self, app_name):
        """Class constructor."""
        self.port = os.getenv("SERVER_PORT")
        self.host = os.getenv("SERVER_HOST")
        logging.log_info(
            app_name,
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        pass

    def run(self):
        """Run."""
        server_address = (self.host, int(self.port))
        try:
            httpd = socketserver.TCPServer(
                server_address,
                RequestHandler
                )
        except Exception as e:
            logging.log_error(
                e,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        logging.log_info(
            "Server Up at {}:{}".format(self.host, self.port),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()


if __name__ == '__main__':
    """Main b.e. admin start."""
    try:
        load_dotenv(find_dotenv())
        service_name = os.getenv("SERVICE_NAME")
        app = app(service_name)
        app.run()
    except KeyboardInterrupt:
        logging.log_info(
            "Intercepted KeyboardInterrupt close {}".format(service_name),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        del app
        sys.exit()
