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
"""HTTP Client."""
import os
import sys
import re
import json
from vendor.mucca_logging.mucca_logging import logging
import http.client


class client():
    """http client class."""

    def __init__(self, host, port):
        """Init."""
        self.host = host
        self.port = self.__getApiPort()
        self.client = http.client.HTTPConnection(self.host, self.port)
        self.auth_serv = os.getenv('AUTH_SERV')
        self.headers = {'Content-Type': 'application/json'}

    def __getApiPort(self):
        """Get apigateway port."""
        # dir = ''./vendor/builder/netmucca/.portlist'
        dir = '../muccapp/mucca_install/vendor/builder/netmucca/.portlist'
        with open(dir) as file:
            port_list = file.read()
            try:
                search = re.search(r'apigateway:[0-9]\d{3,5}', port_list, re.I)
                port = search.group().split(':', 5)
                return port[1]
            except Exception as e:
                logging.log_error(
                    e,
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                return None

    def __getToken(self, data):
        try:
            return json.loads(data.decode())["token"]
        except json.decoder.JSONDecodeError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        except KeyError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def __getKey(self, data):
        try:
            return json.loads(data.decode())["key"]
        except json.decoder.JSONDecodeError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        except KeyError as emsg:
            logging.log_error(
                emsg,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def authenticate(self, data):
        """Authenticate user."""
        method = "POST"
        url = self.auth_serv + "/authentication"
        body = json.dumps(data)
        try:
            self.client.request(method, url, body, self.headers)
            logging.log_info(
                "Authentication...",
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            response = self.client.getresponse().read()
            return self.authorize(response)
        except Exception as e:
            logging.log_error(
                e,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None

    def authorize(self, res):
        """Authorize user."""
        method = "GET"
        url = self.auth_serv + "/authorization"
        body = ""
        headers = {
            'Content-Type': 'application/json',
            'token': self.__getToken(res),
            'key': self.__getKey(res)
            }
        try:
            self.client.request(method, url, body, headers)
            logging.log_info(
                "Authorization...",
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return self.client.getresponse().read()
        except Exception as e:
            logging.log_error(
                e,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None
        pass

    def logout(self, res):
        """Logout user."""
        method = "GET"
        url = self.auth_serv + "/logout"
        body = ""
        headers = {
            'Content-Type': 'application/json',
            'token': self.__getToken(res),
            'key': self.__getKey(res)
            }
        try:
            self.client.request(method, url, body, headers)
            logging.log_info(
                "Authorization...",
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return self.client.getresponse().read()
        except Exception as e:
            logging.log_error(
                e,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None
        pass
