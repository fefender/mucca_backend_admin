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
from bson.json_util import dumps
from http.server import BaseHTTPRequestHandler
from vendor.mucca_logging.mucca_logging import logging
from src.routes.routes import router
from src.request.request import request


class RequestHandler(BaseHTTPRequestHandler):
    """Extend base http servers."""

    def do_POST(self):
        """Post."""
        logging.log_info(
            "Server received POST request",
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        new_request = request(self)
        new_router = router(new_request)
        status, msg = new_router.rout()
        self.respond(status, msg)
        return

    def do_GET(self):
        """Get."""
        logging.log_info(
            "Server received GET request",
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        new_request = request(self)
        new_router = router(new_request)
        status, msg = new_router.rout()
        self.respond(status, msg)
        return

    def respond(self, status, msg):
        """Response."""
        self.send_response(status)
        self.send_header("Content-type", "application/json;charset=utf-8")
        self.end_headers()
        res = json.loads(msg)
        response = dumps(res).encode()
        logging.log_info(
            "Respond with status {}".format(status),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return self.wfile.write(response)

    # def handle_http(self, status, content_type):
    #     """Handler."""
    #     self.send_response(status)
    #     self.send_header("Content-type", "application/json;charset=utf-8")
    #     self.end_headers()
    #     logging.log_info(
    #         "status {} content {}".format(status, content_type),
    #         os.path.abspath(__file__),
    #         sys._getframe().f_lineno
    #     )
    #     return bytes("Suca", 'UTF-8')
