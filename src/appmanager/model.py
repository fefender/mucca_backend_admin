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
"""Datamodel class."""
import os
import sys
import json
from vendor.mucca_logging.mucca_logging import logging


class model():
    """Datamodel class."""

    def __init__(self, env):
        """Init."""
        self.env = env
        self.environments = ['develop', 'production', 'stage']
        # self.file_name = '/config.json'
        # self.partial_path = './app/datamodel/mpkg/'
        # '../muccapp/mucca_install/app/datamodel/mpkg/'
        self.partial_path = os.getenv('MODEL_PATH')

    def __newFolder(self, name):
        path = self.env + "/" + name
        try:
            os.mkdir(self.partial_path + path)
        except Exception as e:
            logging.log_warning(
                '{}'.format(e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None
        path = path + "/" + "datamodel"
        try:
            os.mkdir(self.partial_path + path)
        except Exception as e:
            logging.log_warning(
                '{}'.format(e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None
        return True

    def set(self, key, data):
        """Setter."""
        try:
            new_model = dict()
            schema_obj = dict({"$jsonSchema": {
                "bsonType": "object",
                "required": data['required'],
                "properties": data['properties']}})
            datamap = dict({"datamapping": schema_obj})
            new_model.update(datamap)
            unindx = dict({"uniqueindex": data['uniqueindex']})
            new_model.update(unindx)
            model = json.dumps(new_model, indent=3, sort_keys=True)
        except Exception as e:
            logging.log_warning(
                '{}'.format(e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
                )
            return None
        name = data['modelname']
        last_half = "/" + name + "/datamodel"
        file_name = "/" + name + '.json'
        if self.env in self.environments:
            try:
                path = self.partial_path + self.env + last_half + file_name
                check = open(path)
                check.close()
            except Exception as e:
                logging.log_warning(
                    '{} does not exist.{}.Exec --build first.'.format(name, e),
                    os.path.abspath(__file__),
                    sys._getframe().f_lineno
                    )
                new_fold = self.__newFolder(name)
                if new_fold is None:
                    return None
            with open(path, "w") as mod:
                try:
                    wr = mod.write(model)
                    # m_name = mod.name
                    mod.close()
                    return json.dumps({"createdfile": "datamodel"})
                except Exception as e:
                    logging.log_warning(
                        'Bad request.{}'.format(e),
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                        )
                    return None
        logging.log_warning(
            'Bad request.',
            os.path.abspath(__file__),
            sys._getframe().f_lineno
            )
        return None

    def get(self, name):
        """Getter."""
        last_half = "/" + name + "/datamodel"
        file_name = "/" + name + '.json'
        if self.env in self.environments:
            path = self.partial_path + self.env + last_half + file_name
            try:
                with open(path) as file:
                    config = json.load(file)
                    file.close()
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
