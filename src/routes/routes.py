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
import json
import re
from vendor.mucca_logging.mucca_logging import logging
from src.client.client import client


class router():
    """Class router."""

    def __init__(self, path, request):
        """init."""
        self.path = path
        self.request = request
        self.paths = ['authorization', 'authentication', 'logout']
        self.actions = ['read', 'create', 'update', 'delete']
        self.check_a = False
        self.check_p = False

    def __getApiPort(self):
        """Get apigateway port."""
        # dir = ''./vendor/builder/netmucca/.portlist'
        dir = '../muccapp/mucca_install/vendor/builder/netmucca/.portlist'
        with open(dir) as file:
            port_list = file.read()
            try:
                search = re.search(r'apigateway:[0-9]\d{3,5}', port_list, re.I)
                port = search.group().split(':', 5)
                return int(port[1])
            except Exception as e:
                logging.log_error(
                    e,
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                return None

    def rout(self):
        """Rout method."""
        if self.path in self.paths:
            logging.log_info(
                "{}, calling client".format(self.path),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            new_client = client("localhost", self.__getApiPort(), self.request)
            func = getattr(new_client, self.path)
            func()
        else:
            self.check_p = True
        if self.path in self.actions:
            logging.log_info(
                "{}, calling controller".format(self.path),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        else:
            self.check_a = True
        if self.check_a & self.check_p:
            logging.log_warning(
                'Bad request',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            pass
