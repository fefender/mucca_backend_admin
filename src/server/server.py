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
"""Server."""
import os
import sys
import json
from http.server import BaseHTTPRequestHandler
from vendor.mucca_logging.mucca_logging import logging
from src.routes.routes import router


class RequestHandler(BaseHTTPRequestHandler):
    """Extend base http servers."""

    def do_HEAD(self):
        """head."""
        logging.log_info(
            "head",
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return

    def do_POST(self):
        """Post."""
        logging.log_info(
            "Server received POST request",
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        rout = router(self.__formatPath(self.path), post_body)
        rout.rout()
        # print(json.loads(post_body.decode()))
        return

    def do_GET(self):
        """Get."""
        # self.respond()
        # self.send_response(200, 'OK')
        logging.log_info(
            "Server received GET request",
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        rout = router(self.__formatPath(self.path), post_body)
        rout.rout()
        self.respond()
        return

    def handle_http(self, status, content_type):
        """Handler."""
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        logging.log_info(
            "status {} content {}".format(status, content_type),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        # print(self.path)
        # route_content = routes[self.path]
        return bytes("Suca", 'UTF-8')

    def respond(self):
        """Response."""
        content = self.handle_http(200, "text/html")
        self.wfile.write(content)
        return

    def __formatPath(self, path):
        """Format path."""
        try:
            my_path = path.split("/")
            return my_path[1]
        except Exception as e:
            logging.log_error(
                e,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
