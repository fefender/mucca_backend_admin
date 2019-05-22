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
"""Request class."""
import os
import sys
import json
from vendor.mucca_logging.mucca_logging import logging


class request():
    """Request."""

    def __init__(self, request):
        """Init."""
        self.method = request.command
        self.uri = request.path
        self.version = self.getVersion()
        self.headers = request.headers
        self.content_len = self.__checkContentLength()
        # self.content_len = int(self.headers.get('Content-Length'))
        self.body = request.rfile.read(self.content_len)

    def __checkContentLength(self):
        """Check if content_len exists."""
        if self.headers.get('Content-Length'):
            return int(self.headers.get('Content-Length'))
        else:
            return 0

    def getMethod(self):
        """getMethod."""
        return self.method

    def setMethod(self, method):
        """getMethod."""
        self.method = method
        return self.method

    def getVersion(self):
        """getMethod."""
        path = self.uri.split('/')
        return path[1]

    def setVersion(self, version):
        """getMethod."""
        self.version = version
        return self.version

    def getUri(self):
        """getMethod."""
        path = self.uri.split('/')
        if len(path) > 1:
            return path[2]
        else:
            return None

    def setUri(self, uri):
        """getMethod."""
        self.uri = uri
        return self.uri

    def getAction(self):
        """getMethod."""
        path = self.uri.split('/')
        if len(path) > 2:
            return path[2]
        else:
            return None

    def setAction(self, uri):
        """getMethod."""
        self.uri = uri
        return self.uri

    def getEnv(self):
        """getMethod."""
        path = self.uri.split('/')
        if len(path) > 3:
            return path[3]
        else:
            return None

    def setEnv(self, uri):
        """getMethod."""
        self.uri = uri
        return self.uri

    def getQuery(self):
        """getMethod."""
        path = self.uri.split('/')
        if len(path) > 4:
            if "=" in path[4]:
                return self.getValues(path[4])
            return path[4]
        else:
            return None

    def setQuery(self, uri):
        """getMethod."""
        self.uri = uri
        return self.uri

    def getValues(self, query):
        """Get values in query."""
        arr = query.split('=')
        name = arr[0]
        values = arr[1]
        return name, values

    def getName(self):
        """getMethod."""
        path = self.uri.split('/')
        if len(path) > 5:
            return path[5]
        else:
            return None

    def setName(self, uri):
        """getMethod."""
        self.uri = uri
        return self.uri

    def getHeaders(self):
        """getMethod."""
        try:
            return self.headers
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
        return self.headers

    def setHeaders(self, headers):
        """getMethod."""
        self.headers = headers
        return self.headers

    def getBody(self):
        """getMethod."""
        if self.content_len > 0:
            try:
                return json.loads(self.body.decode())
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
            return ""

    def setBody(self, body):
        """getMethod."""
        self.body = body
        return self.body
