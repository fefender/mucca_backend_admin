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
"""Router."""
# routes = {
#     '/': 'Hello World',
#     '/goodbye': 'Goodbye World'
#     }
import os
import sys
from vendor.mucca_logging.mucca_logging import logging
from src.client.client import client
from src.repository.repository import repository


class router():
    """Class router."""

    def __init__(self, request_instance):
        """init."""
        # self.path = path
        self.request = request_instance
        self.paths = ['authorization', 'authentication', 'logout']
        self.actions = ['read', 'create', 'update', 'delete']
        self.check_a = False
        self.check_p = False

    def rout(self):
        """Rout method."""
        if self.request.getVersion() == os.getenv('SERVICE_VERSION'):
            if self.request.getUri() in self.paths:
                logging.log_info(
                    "calling client",
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                new_client = client(
                    self.request.getHeaders(),
                    self.request.getBody())
                func = getattr(new_client, self.request.getUri())
                return func()
            else:
                self.check_p = True
            if self.request.getUri() in self.actions:
                logging.log_info(
                    "{}, calling repository",
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                new_repository = repository()
                func = getattr(new_repository, self.request.getUri())
                return func(self.request.getQuery(), self.request.getBody())
            else:
                self.check_a = True
            if self.check_a & self.check_p:
                logging.log_warning(
                    'Bad request',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                return None
        else:
            logging.log_warning(
                'Bad request',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None
