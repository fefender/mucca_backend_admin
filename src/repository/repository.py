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
"""Controller."""
import os
import sys
import json
from vendor.mucca_logging.mucca_logging import logging


class repository():
    """Controller class."""

    def __init__(self):
        """Init."""
        self.environments = ['develop', 'production', 'stage']
        pass

    def __getRequestEnvironement(self, data):
        """Get requested environment."""
        try:
            return data["environment"]
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

    def __getConfig(self, env):
        """Get admin username."""
        # partial_path = './app/config/'
        partial_path = '../muccapp/mucca_install/app/config/'
        file_name = '/config.json'
        if env in self.environments:
            path = partial_path + env + file_name
            with open(path) as file:
                config = json.load(file)
                return json.dumps(config)
        else:
            logging.log_warning(
                'Bad request',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None

    def create(self, query, data):
        """Create."""
        env = self.__getRequestEnvironement(data)
        pass

    def read(self, query, data):
        """Read."""
        env = self.__getRequestEnvironement(data)
        try:
            conf = self.__getConfig(env)
            if conf:
                status = 200
                return status, conf
        except Exception as e:
            logging.log_error(
                e,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None

    def update(self, query, data):
        """Update."""
        env = self.__getRequestEnvironement(data)
        pass

    def delete(self, query, data):
        """Delete."""
        env = self.__getRequestEnvironement(data)
        pass
