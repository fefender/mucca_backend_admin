# Copyright 2018 Federica Cricchio
# fefender@gmail.com
#
# This file is part of mucca_registry.
#
# mucca_registry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mucca_registry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mucca_registry.  If not, see <http://www.gnu.org/licenses/>.
"""Mucca Boot."""
import os
import sys
from src.session.repository.repository import repository
from vendor.mucca_logging.mucca_logging import logging
from src.session.mongo_connection.mongo_connection import mongo_connection


class boot:
    """Boot Class."""

    @staticmethod
    def init():
        """Init."""
        client_address = os.getenv("MONGO_CLIENT")
        mongo_connection_instance = mongo_connection(client_address)
        boot_repo = repository(mongo_connection_instance)
        if boot_repo.dbCheck() is False:
            logging.log_info(
                'Creating database',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            boot_repo.collectionCheck()
        logging.log_info(
            'Repository booted',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        mongo_connection_instance.closeConnection()
        del boot_repo
        return True
