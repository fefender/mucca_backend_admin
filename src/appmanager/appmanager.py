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
from src.response.response import response
from src.appmanager.config import config
from src.appmanager.model import model
from importlib import import_module


class appmanager():
    """Controller class."""

    def __init__(self, request_instance):
        """Init."""
        # self.environments = ['develop', 'production', 'stage']
        self.queries = ['config', 'model', 'portlist']
        self.request = request_instance
        self.env = self.request.getEnv()
        self.query = self.request.getQuery()

    def create(self):
        """Create."""
        if self.query in self.queries:
            print("IF---CrEATE APP MANAGER")
            clss = getattr(
                import_module("src.appmanager." + self.query),
                self.query)
            instance = clss(self.env)
            func = getattr(instance, "set")
            resp = func(self.request.getName(), self.request.getBody())
            if resp is not None:
                return response.respond(200, resp)
            return response.respond(404, None)
        return response.respond(404, None)

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
        return response.respond(400, None)

    def update(self):
        """Update."""
        pass

    def delete(self):
        """Delete."""
        pass
