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
from src.appmanager.config import config
from src.appmanager.model import model
from importlib import import_module


class appmanager():
    """Controller class."""

    def __init__(self, request_instance):
        """Init."""
        self.environments = ['develop', 'production', 'stage']
        self.queries = ['config', 'model', 'portlist']
        self.request = request_instance
        self.env = self.request.getEnv()
        self.query = self.request.getQuery()
        pass
    #
    # def __getConfig(self, env):
    #     """Get admin username."""
    #     # partial_path = './app/config/'
    #     partial_path = '../muccapp/mucca_install/app/config/'
    #     file_name = '/config.json'
    #     if env in self.environments:
    #         path = partial_path + env + file_name
    #         try:
    #             with open(path) as file:
    #                 config = json.load(file)
    #                 file.close()
    #                 return json.dumps(config)
    #         except Exception as e:
    #             logging.log_warning(
    #                 'Not found.{}'.format(e),
    #                 os.path.abspath(__file__),
    #                 sys._getframe().f_lineno
    #                 )
    #             return None
    #     else:
    #         logging.log_warning(
    #             'Not found.{}'.format(e),
    #             os.path.abspath(__file__),
    #             sys._getframe().f_lineno
    #             )
    #         return None
    #
    # def __setConfig(self):
    #     """Add new Service to config file."""
    #     config = self.__getConfig(self.env)
    #     c = json.loads(config)
    #     c_mpkg = c['mpkg']
    #     body = self.request.getBody()
    #     basic = {
    #       "name": self.request.getName(),
    #       "git": "https://github.com/RiccardoCurcio/mucca_crud_py.git",
    #       "owner": "RiccardoCurcio",
    #       "reponame": "mucca_crud_py",
    #       "branch": "develop",
    #       "baseimage": "mucca-py",
    #       "datamodel": body['datamodel'],
    #       "ownerfilter": body['ownerfilter'],
    #       "protocol": "udp",
    #       "pyrequirements": [
    #         "python-dotenv",
    #         "pymongo",
    #         "tzlocal"
    #       ]
    #       }
    #     c_mpkg.append(basic)
    #     c.update({"mpkg": c_mpkg})
    #     new_conf = json.dumps(c, indent=1)
    #     # partial_path = './app/config/'
    #     partial_path = '../muccapp/mucca_install/app/config/'
    #     file_name = '/config.json'
    #     path = partial_path + self.env + file_name
    #     try:
    #         with open(path, "w") as file:
    #             wr = file.write(new_conf)
    #             file.close()
    #             return wr
    #     except Exception as e:
    #         logging.log_warning(
    #             'Not found.{}'.format(e),
    #             os.path.abspath(__file__),
    #             sys._getframe().f_lineno
    #             )
    #         return None
    #
    # def __getDataModel(self, env):
    #     if self.request.getName():
    #         # partial_path = './app/datamodel/mpkg/'
    #         partial_path = '../muccapp/mucca_install/app/datamodel/mpkg/'
    #         name = self.request.getName()
    #         last_half = "/" + name + "/datamodel/"
    #         file_name = name + '.json'
    #         if env in self.environments:
    #             path = partial_path + env + last_half + file_name
    #             try:
    #                 with open(path) as file:
    #                     config = json.load(file)
    #                     file.close()
    #                     return json.dumps(config)
    #             except Exception as e:
    #                 logging.log_warning(
    #                     'Not found',
    #                     os.path.abspath(__file__),
    #                     sys._getframe().f_lineno
    #                     )
    #                 return None
    #     logging.log_warning(
    #         'Not Found.{}'.format(e),
    #         os.path.abspath(__file__),
    #         sys._getframe().f_lineno
    #         )
    #     return None
    #
    # def __setDataModel(self):
    #     """Set new data model."""
    #     body = self.request.getBody()
    #     try:
    #         new_model = dict()
    #         schema_obj = dict({"$jsonSchema": {
    #             "bsonType": "object",
    #             "required": body['required'],
    #             "properties": body['properties']}})
    #         datamap = dict({"datamapping": schema_obj})
    #         new_model.update(datamap)
    #         unindx = dict({"uniqueindex": []})
    #         new_model.update(unindx)
    #         model = json.dumps(new_model, indent=3, sort_keys=True)
    #     except Exception as e:
    #         logging.log_warning(
    #             'Bad request.{}'.format(e),
    #             os.path.abspath(__file__),
    #             sys._getframe().f_lineno
    #             )
    #         return None
    #     # partial_path = './app/datamodel/mpkg/'
    #     partial_path = '../muccapp/mucca_install/app/datamodel/mpkg/'
    #     name = self.request.getName()
    #     # mod_name = body['modelname'] + ".json"
    #     last_half = "/" + name + "/datamodel/"
    #     file_name = name + '.json'
    #     if self.env in self.environments:
    #         try:
    #             path = partial_path + self.env + last_half
    #             check = open(path)
    #         except Exception as e:
    #             logging.log_warning(
    #                 'Bad request.{} does not exist.{}'.format(name, e),
    #                 os.path.abspath(__file__),
    #                 sys._getframe().f_lineno
    #                 )
    #             return None
    #         check.close()
    #         # path = '../muccapp/mucca_install/app/datamodel/mpkg/develop/cani/datamodel/'
    #         with open(path + file_name, "w") as mod:
    #             try:
    #                 wr = mod.write(model)
    #                 mod.close()
    #                 return wr
    #             except Exception as e:
    #                 logging.log_warning(
    #                     'Bad request.{}'.format(e),
    #                     os.path.abspath(__file__),
    #                     sys._getframe().f_lineno
    #                     )
    #                 return None
    #     logging.log_warning(
    #         'Bad request.{}'.format(e),
    #         os.path.abspath(__file__),
    #         sys._getframe().f_lineno
    #         )
    #     return None
    #
    # def __getPortList(self):
    #     """Get apigateway port."""
    #     # dir = ''./vendor/builder/netmucca/.portlist'
    #     dir = '../muccapp/mucca_install/vendor/builder/netmucca/.portlist'
    #     try:
    #         with open(dir) as file:
    #             port_list = file.read()
    #             arr = re.findall('[a-z?_]+:+[0-9]+:+[a-z]', port_list)
    #             file.close()
    #         return self.__getPortByEnv(arr)
    #     except Exception as e:
    #         logging.log_warning(
    #             'Not found.{}'.format(e),
    #             os.path.abspath(__file__),
    #             sys._getframe().f_lineno
    #             )
    #         return None
    #
    # def __getPortByEnv(self, list_arr):
    #     """Return port list by env."""
    #     list_d = dict()
    #     if self.env == 'develop':
    #         for x in list_arr:
    #             newarr = x.split(':', 2)
    #             if newarr[2] == 'd':
    #                 el = dict({newarr[0]: newarr[1]})
    #                 list_d.update(el)
    #         list_o = {"develop": list_d}
    #         return json.dumps(list_o)
    #     if self.env == 'production':
    #         for x in list_arr:
    #             newarr = x.split(':', 2)
    #             if newarr[2] == 'p':
    #                 el = dict({newarr[0]: newarr[1]})
    #                 list_d.update(el)
    #         list_o = {"production": list_d}
    #         return json.dumps(list_o)
    #     if self.env == 'stage':
    #         for x in list_arr:
    #             newarr = x.split(':', 2)
    #             if newarr[2] == 's':
    #                 el = dict({newarr[0]: newarr[1]})
    #                 list_d.update(el)
    #         list_o = {"stage": list_d}
    #         return json.dumps(list_o)
    #     return None

    def create(self):
        """Create."""
        if self.query in self.queries:
            clss = getattr(
                import_module("src.appmanager." + self.query),
                self.query)
            instance = clss(self.env)
            func = getattr(instance, "set")
            resp = func(self.request.getName(), self.request.getBody())
            print(resp)
            print(type(resp))
            if resp is not None:
                return response.respond(200, resp)
            return response.respond(404, None)
        # if self.query in self.queries:
        #     if self.query == "model":
        #         mod = self.__setDataModel()
        #         if mod is not None:
        #             return response.respond(200, None)
        #         else:
        #             return response.respond(404, None)
        #     if self.query == "config":
        #         conf = self.__setConfig()
        #         if conf is not None:
        #             return response.respond(200, None)
        #         else:
        #             return response.respond(404, None)
        pass

    def read(self):
        """Read."""
        if self.query in self.queries:
            clss = getattr(
                import_module("src.appmanager." + self.query),
                self.query)
            instance = clss(self.env)
            func = getattr(instance, "get")
            param = self.request.getName()
            if self.query == 'portlist':
                param = None
            resp = func(param)
            if resp is not None:
                return response.respond(200, resp)
            return response.respond(404, None)
            # if self.query == "config":
            #     try:
            #         conf = self.__getConfig(self.env)
            #         if conf is not None:
            #             return response.respond(200, conf)
            #         return response.respond(404, None)
            #     except Exception as e:
            #         logging.log_error(
            #             e,
            #             os.path.abspath(__file__),
            #             sys._getframe().f_lineno
            #             )
            #         return None
            # if self.query == "model":
            #     try:
            #         model = self.__getDataModel(self.env)
            #         if model is not None:
            #             return response.respond(200, model)
            #         return response.respond(404, None)
            #     except Exception as e:
            #         logging.log_error(
            #             e,
            #             os.path.abspath(__file__),
            #             sys._getframe().f_lineno
            #             )
            #         return None
            # if self.query == 'portlist':
            #     try:
            #         list = self.__getPortList()
            #         if list is not None:
            #             return response.respond(200, list)
            #         return response.respond(404, None)
            #     except Exception as e:
            #         logging.log_error(
            #             e,
            #             os.path.abspath(__file__),
            #             sys._getframe().f_lineno
            #             )
            #         return None
            # return response.respond(404, None)
        return response.respond(400, None)

    def update(self):
        """Update."""
        pass

    def delete(self):
        """Delete."""
        pass
