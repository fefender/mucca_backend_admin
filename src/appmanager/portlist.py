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
"""PORTLIST."""
import os
import re
import sys
import json
from vendor.mucca_logging.mucca_logging import logging


class portlist():
    """Portlist class."""

    def __init__(self, env):
        """Init."""
        self.env = env
        self.environments = ['develop', 'production', 'stage']
        # dir = ''./vendor/builder/netmucca/.portlist'
        self.dir = '../muccapp/mucca_install/vendor/builder/netmucca/.portlist'

    def get(self, empty):
        """Get apigateway port."""
        if self.env in self.environments:
            try:
                with open(self.dir) as file:
                    port_list = file.read()
                    arr = re.findall('[a-z?_]+:+[0-9]+:+[a-z]', port_list)
                    file.close()
                return self.__getPortByEnv(arr)
            except Exception as e:
                logging.log_warning(
                    'Not found.{}'.format(e),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                return None
        return None

    def __getPortByEnv(self, list_arr):
        """Return port list by env."""
        list_d = dict()
        if self.env == 'develop':
            for x in list_arr:
                newarr = x.split(':', 2)
                if newarr[2] == 'd':
                    el = dict({newarr[0]: newarr[1]})
                    list_d.update(el)
            list_o = {"develop": list_d}
            return json.dumps(list_o)
        if self.env == 'production':
            for x in list_arr:
                newarr = x.split(':', 2)
                if newarr[2] == 'p':
                    el = dict({newarr[0]: newarr[1]})
                    list_d.update(el)
            list_o = {"production": list_d}
            return json.dumps(list_o)
        if self.env == 'stage':
            for x in list_arr:
                newarr = x.split(':', 2)
                if newarr[2] == 's':
                    el = dict({newarr[0]: newarr[1]})
                    list_d.update(el)
            list_o = {"stage": list_d}
            return json.dumps(list_o)
        return None
