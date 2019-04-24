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
"""Session Repository."""
import os
import sys
import datetime
from bson.objectid import ObjectId
from vendor.mucca_logging.mucca_logging import logging
from src.session.mongo_connection.mongo_connection import mongo_connection


class repository():
    """Session repository class."""

    def __init__(self, connection_instance):
        """Init."""
        self.client_db = os.getenv("CLIENT_DB")
        self.db_collection = os.getenv("DB_COLLECTION")
        self.__mongo_instance = connection_instance
        self.__mongo_instance.setConnection()
        self.client = self.__mongo_instance.getConnection()
        self.db = self.client[self.client_db]
        self.collection = self.db[self.db_collection]

    def dbCheck(self):
        """DbCheck."""
        db_names = self.client.list_database_names()
        if self.client_db not in db_names:
            return False
        return True

    def collectionCheck(self):
        """Check if Collection Exists."""
        collection_names = self.client.list_database_names()
        logging.log_info(
            'Checking if Collection exists...',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        if self.db_collection not in collection_names:
            return False
        return True

    def create(self, user, data):
        """Create."""
        username = user
        token = data['token']
        key = data['key']
        status = "active"
        last_update = datetime.datetime.utcnow()
        add = {
            "username": username,
            "token": token,
            "key": key,
            "status": status,
            "last_update": last_update
            }
        try:
            result = self.collection.insert_one(add).inserted_id
            logging.log_info(
                "Session Created.",
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return True
        except Exception as e:
            logging.log_error(
                'Error {}'.format(e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return False

    def read(self, data):
        """Read."""
        find = {"token": data['token'], "key": data['key']}
        try:
            result = self.collection.find(find)
            logging.log_info(
                'Searching token and key in db',
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        except TypeError as emsg:
            logging.log_error(
                'Type argument error {}'.format(emsg),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
        count = result.count()
        if count is 0:
            return None
        username = result.distinct("username")
        id = result.distinct("_id")
        token = result.distinct("token")
        key = result.distinct("key")
        status = result.distinct("status")
        last_update = result.distinct("last_update")
        response = {"username": username[0],
                    "_id": id[0],
                    "token": token[0],
                    "key": key[0],
                    "status": status[0],
                    "last_update": last_update[0]}
        return response

    def update(self, data):
        """Update."""
        res = self.read(data)
        if res is not None:
            status = res['status']
            last_update = datetime.datetime.utcnow()
            token = res['token']
            key = res['key']
            username = res['username']
            id = res['_id']
            if 'status' in data:
                status = data['status']
            if 'token' in data:
                token = data['token']
            if 'key' in data:
                key = data['key']
            if 'username' in data:
                username = data['username']
            filter = {"_id": ObjectId(id)}
            request = {
                "username": username,
                "token": token,
                "key": key,
                "status": status,
                "last_update": last_update
                }
            update = {"$set": request}
            try:
                result = self.collection.update_one(filter, update)
                logging.log_info(
                    "Session Updated...",
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return True
            except Exception as emsg:
                logging.log_error(
                    'Updating fail. {}'.format(emsg),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                )
                return False
