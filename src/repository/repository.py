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
import re
import sys
import json
from src.response.response import response
from vendor.mucca_logging.mucca_logging import logging


class repository():
    """Controller class."""

    def __init__(self, request_instance):
        """Init."""
        self.environments = ['develop', 'production', 'stage']
        self.queries = ['config', 'model', 'portlist']
        self.request = request_instance
        self.env = self.request.getEnv()
        self.query = self.request.getQuery()
        pass

    def __getConfig(self, env):
        """Get admin username."""
        # partial_path = './app/config/'
        partial_path = '../muccapp/mucca_install/app/config/'
        file_name = '/config.json'
        if env in self.environments:
            path = partial_path + env + file_name
            try:
                with open(path) as file:
                    config = json.load(file)
                    return json.dumps(config)
            except Exception as e:
                logging.log_warning(
                    'Not found.{}'.format(e),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                return None
        else:
            logging.log_warning(
                'Not found.{}'.format(e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None

    def __getDataModel(self, env):
        if self.request.getName():
            # partial_path = './app/datamodel/mpkg/'
            partial_path = '../muccapp/mucca_install/app/datamodel/mpkg/'
            name = self.request.getName()
            last_half = "/" + name + "/datamodel/"
            file_name = name + '.json'
            if env in self.environments:
                path = partial_path + env + last_half + file_name
                try:
                    with open(path) as file:
                        config = json.load(file)
                        return json.dumps(config)
                except Exception as e:
                    logging.log_warning(
                        'Not found',
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                        )
                    return None
        logging.log_warning(
            'Not Found.{}'.format(e),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        return None

    def __getPortList(self):
        """Get apigateway port."""
        # dir = ''./vendor/builder/netmucca/.portlist'
        dir = '../muccapp/mucca_install/vendor/builder/netmucca/.portlist'
        try:
            with open(dir) as file:
                port_list = file.read()
                arr = re.findall('[a-z]+:+[0-9]+:+[a-z]', port_list)
            return self.__getPortByEnv(arr)
        except Exception as e:
            logging.log_warning(
                'Not found.{}'.format(e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None

    def __getPortByEnv(self, list_arr):
        """Returns port list by env."""
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

    def create(self):
        """Create."""
        pass

    def read(self):
        """Read."""
        if self.query in self.queries:
            if self.query == "config":
                try:
                    conf = self.__getConfig(self.env)
                    if conf is not None:
                        return response.respond(200, conf)
                    else:
                        return response.respond(404, None)
                except Exception as e:
                    logging.log_error(
                        e,
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                        )
                    return None
            if self.query == "model":
                try:
                    model = self.__getDataModel(self.env)
                    if model is not None:
                        return response.respond(200, model)
                    else:
                        return response.respond(404, None)
                except Exception as e:
                    logging.log_error(
                        e,
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                        )
                    return None
            if self.query == 'portlist':
                try:
                    list = self.__getPortList()
                    if list is not None:
                        return response.respond(200, list)
                    else:
                        return response.respond(404, None)
                except Exception as e:
                    logging.log_error(
                        e,
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                        )
                    return None
        else:
            return response.respond(404, None)

    def update(self):
        """Update."""
        pass

    def delete(self):
        """Delete."""
        pass
