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
from src.session.mongo_connection.mongo_connection import mongo_connection


class RequestHandler(BaseHTTPRequestHandler):
    """Extend base http servers."""

    def __init__(self, request, client_address, server):
        """Init."""
        self.client_address = os.getenv("MONGO_CLIENT")
        self.mongo_connection_instance = mongo_connection(self.client_address)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_OPTIONS(self):
        """Option."""
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_POST(self):
        """Post."""
        new_request = request(self)
        new_router = router(new_request, self.mongo_connection_instance)
        status, msg = new_router.rout()
        self.respond(status, msg)
        return

    def do_GET(self):
        """Get."""
        new_request = request(self)
        new_router = router(new_request, self.mongo_connection_instance)
        status, msg = new_router.rout()
        self.respond(status, msg)
        return

    def respond(self, status, msg):
        """Response."""
        self.send_response(status)
        self.send_header("Content-type", "application/json;charset=utf-8")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()
        return self.wfile.write(msg.encode())

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
