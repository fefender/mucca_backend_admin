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
from src.response.codes import codes


class response():
    """Response class."""

    @staticmethod
    def respond(status, message):
        """Set response."""
        if status in codes:
            default_msg = codes[status]
            response = dict({"message": default_msg})
            if message is not None:
                msg = dict({'data': json.loads(message)})
                response.update(msg)
        logging.log_info(
            "Response status {}:{}".format(status, default_msg),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return status, json.dumps(response)
