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
import datetime
from datetime import timedelta
from vendor.mucca_logging.mucca_logging import logging
from src.session.repository.repository import repository
import http.client


class auth():
    """http client class."""

    def __init__(self, header, body, mongo_instance):
        """Init."""
        self.host = os.getenv('CLIENT_HOST')
        self.port = self.__getApiPort()
        self.client = http.client.HTTPConnection(self.host, self.port)
        self.mongo_connection_instance = mongo_instance
        self.session_instance = repository(self.mongo_connection_instance)
        self.auth_serv = os.getenv('AUTH_SERV')
        self.headers = {"Content-Type": "application/json;charset=utf-8"}
        self.request = body
        self.req_header = header
        self.environments = ['develop', 'production', 'stage']

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

    def __getRequestEnvironement(self):
        """Get requested environment."""
        try:
            return self.request["environment"]
        except Exception as emsg:
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

    def __getAdminUsername(self):
        """Get admin username."""
        # partial_path = './app/config/'
        partial_path = '../muccapp/mucca_install/app/config/'
        file_name = '/config.json'
        env = self.__getRequestEnvironement()
        if env in self.environments:
            path = partial_path + env + file_name
            with open(path) as file:
                config = json.load(file)
                return config['superowner']
        else:
            logging.log_warning(
                'Bad request',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None

    def __sessionAuth(self, data):
        """Verify session."""
        user_info = self.session_instance.read(data)
        if user_info is not None:
            if self.__sessionTimeCheck(user_info['last_update']) is True:
                logging.log_info(
                    'Session Valid',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                try:
                    up_res = self.session_instance.update(data)
                except Exception as e:
                    logging.log_error(
                        e,
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                        )
                status = 200
                msg = "ok"
                return status, msg
            else:
                logging.log_warning(
                    'Session Expired',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                update = {
                    "token": data['token'],
                    "key": data['key'],
                    "status": "expired"}
                try:
                    up_res = self.session_instance.update(update)
                except Exception as e:
                    logging.log_error(
                        e,
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                        )
                status = 401
                msg = "Anauthorized User"
                return status, msg
        status = "not found"
        msg = "not found"
        return status, msg

    def __sessionTimeCheck(self, time):
        """Check if session is stil valid."""
        now = datetime.datetime.utcnow()
        limit = os.getenv('SESSION_TTL_H')
        delta = timedelta(hours=-int(limit))
        if time > now + delta:
            return True
        return False

    def authentication(self):
        """Authenticate user."""
        if self.__getAdminUsername() == self.request["username"]:
            method = "POST"
            url = self.auth_serv + "/authentication"
            body = {
                "username": self.request['username'],
                "password": self.request['password']
                }
            try:
                self.client.request(
                    method,
                    url,
                    json.dumps(body),
                    self.headers)
                logging.log_info(
                    "Authentication...",
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                response_obj = self.client.getresponse()
                msg = response_obj.read().decode('utf-8')
                status = response_obj.status
                # return status, msg
            except Exception as e:
                logging.log_error(
                    e,
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
            if status == 201:
                s_resp = self.session_instance.create(json.loads(msg))
            return status, msg
        else:
            # Sistemare Risposte
            status = 401
            msg = "Anauthorized User"
            return status, msg

    def authorization(self):
        """Authorize user."""
        method = "GET"
        url = self.auth_serv + "/authorization"
        body = ""
        headers = {
            'Content-Type': 'application/json',
            'token': self.req_header['token'],
            'key': self.req_header['key']
            }
        try:
            self.client.request(method, url, body, headers)
            logging.log_info(
                "Authorization...",
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            response_obj = self.client.getresponse()
            msg = response_obj.read().decode('utf-8')
            status = response_obj.status
            if status == 200:
                data = {
                    'token': self.req_header['token'],
                    'key': self.req_header['key']
                    }
                s_res = self.session_instance.update(data)
            return status, msg
        except Exception as e:
            logging.log_error(
                e,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
        # [2019-04-19 18:30:17]
        #  ERROR AdminBackEnd /home/fefe/Develop/mucca-project
        # /mucca_backend_admin/src/auth/auth.py:133
        # "Remote end closed connection without response"
            data = {
                'token': self.req_header['token'],
                'key': self.req_header['key']
                }
            return self.__sessionAuth(data)
        pass

    def logout(self):
        """Logout user."""
        method = "GET"
        url = self.auth_serv + "/logout"
        body = ""
        headers = {
            'Content-Type': 'application/json',
            'token': self.req_header['token'],
            'key': self.req_header['key']
            }
        try:
            self.client.request(method, url, body, headers)
            logging.log_info(
                "Logging out...",
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            response_obj = self.client.getresponse()
            msg = response_obj.read().decode('utf-8')
            status = response_obj.status
            if status == 200:
                data = {"status": "expired"}
                s_res = self.session_instance.update(json.loads(data))
            return status, msg
        except Exception as e:
            logging.log_error(
                e,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            data = {"status": "expired"}
            s_res = self.session_instance.update(json.loads(data))
            return None
        pass
