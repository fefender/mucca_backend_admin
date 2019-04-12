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
"""Response class."""
import os
import sys
import json
from vendor.mucca_logging.mucca_logging import logging


class response():
    """Response class."""

    def __init__(self, status, message):
        """Init."""
        self.status = status
        self.message = message

    def setResponse(self):
        """Set response."""
        try:
            return self.__statusCode(self.status)
        except Exception as e:
            logging.log_error(
                e,
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None

    def __statusCode(self, code):
        """Status code."""
        codes = {
            200: self.__okRes(),
            201: self.__createdRes(),
            400: self.__badRequestRes(),
            401: self.__unauthorizedRes(),
            404: self.__notFoundRes(),
            500: "internal server error"
            }
        func = codes.get(code, lambda: "Invalid status")
        return func()

    def __okRes(self):
        """200."""
        if self.message.Length() > 1:
            return self.message
        else:
            res = {'message': 'success'}
            return str(res)

    def __createdRes(self):
        """201."""
        pass

    def __badRequestRes(self):
        """400."""
        res = {'message': 'unauthorized'}
        return str(res)

    def __unauthorizedRes(self):
        """401."""
        res = {'message': 'bad request'}
        return str(res)

    def __notFoundRes(self):
        """404."""
        res = {'message': 'not found'}
        return str(res)

    def __errorRes(self):
        """500."""
        res = {'message': 'internal server error'}
        return str(res)
