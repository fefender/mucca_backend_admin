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
from src.auth.auth import auth
from src.response.response import response
from src.appmanager.appmanager import appmanager
from src.triggers.triggers import triggers


class router():
    """Class router."""

    def __init__(self, request_instance, mongo_instance):
        """init."""
        self.request = request_instance
        self.mongo_connection_instance = mongo_instance
        self.routes = {
            "auth": ['authorization', 'authentication', 'logout'],
            "actions": ['read', 'create', 'update', 'delete'],
            "triggers": ['list', 'stop', 'run', 'build', 'status', 'logs']
            }

    def rout(self):
        """Rout method."""
        if self.request.getVersion() == os.getenv('SERVICE_VERSION'):
            if self.request.getUri() in self.routes['auth']:
                logging.log_info(
                    "calling Auth",
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                new_auth = auth(
                    self.request.getHeaders(),
                    self.request.getBody(),
                    self.mongo_connection_instance)
                func = getattr(new_auth, self.request.getUri())
                return func()
            if self.request.getUri() in self.routes['actions']:
                new_auth = auth(
                    self.request.getHeaders(),
                    self.request.getBody(),
                    self.mongo_connection_instance)
                status, msg = new_auth.authorization()
                if status == 200:
                    logging.log_info(
                        " calling appmanager",
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                    )
                    new_appmanager = appmanager(self.request)
                    func = getattr(new_appmanager, self.request.getUri())
                    return func()
                else:
                    return response.respond(401, None)
            if self.request.getUri() in self.routes['triggers']:
                new_auth = auth(
                    self.request.getHeaders(),
                    self.request.getBody(),
                    self.mongo_connection_instance)
                status, msg = new_auth.authorization()
                if status == 200:
                    logging.log_info(
                        " calling triggers",
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                    )
                    new_triggers = triggers(self.request)
                    return new_triggers.trigger()
                else:
                    return response.respond(401, None)
            if self.request.getUri() not in self.routes:
                logging.log_warning(
                    'Bad request',
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                return response.respond(400, None)
        else:
            logging.log_warning(
                'Bad request',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return response.respond(400, None)
