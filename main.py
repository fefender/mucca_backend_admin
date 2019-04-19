# Copyright 2019 Federica Cricchio
# fefender@gmail.com
#
# This file is part of mucca_backend_admin.
#
# mucca_backend_admin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mucca_backend_admin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mucca_backend_admin.  If not, see <http://www.gnu.org/licenses/>.
"""Mucca Back End Admin."""

import socketserver
# import http.server
from dotenv import load_dotenv
from dotenv import find_dotenv
import os
import sys
from src.server.server import RequestHandler
from vendor.mucca_logging.mucca_logging import logging
from src.session.boot.boot import boot
# from src.mongo_connection.mongo_connection import mongo_connection


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
        boot.init()
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
