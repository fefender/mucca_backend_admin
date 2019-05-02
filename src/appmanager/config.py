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


class config():
    """Config class."""

    def __init__(self, env):
        """Init."""
        self.env = env
        self.environments = ['develop', 'production', 'stage']
        self.file_name = '/config.json'
        # self.partial_path = './app/config/'
        self.partial_path = '../muccapp/mucca_install/app/config/'
        self.full_path = self.partial_path + self.env + self.file_name

    def set(self, key, data):
        """Setter."""
        if self.env in self.environments:
            config = self.get(None)
            c = json.loads(config)
            # if key in self.keys['mpkg', 'superowner', etc]
            # chiama il rispettivo self.mpkg(data), self.superowner(data)
            if key == "mpkg":
                c_mpkg = c['mpkg']
                basic = {
                  "name": data['modelname'],
                  "git": "https://github.com/RiccardoCurcio/mucca_crud_py.git",
                  "owner": "RiccardoCurcio",
                  "reponame": "mucca_crud_py",
                  "branch": "develop",
                  "baseimage": "mucca-py",
                  "datamodel": data['datamodel'],
                  "ownerfilter": data['ownerfilter'],
                  "protocol": "udp",
                  "pyrequirements": [
                    "python-dotenv",
                    "pymongo",
                    "tzlocal"
                  ]
                  }
                c_mpkg.append(basic)
                c.update({"mpkg": c_mpkg})
                new_conf = json.dumps(c, indent=1)
                try:
                    with open(self.full_path, "w") as file:
                        wr = file.write(new_conf)
                        # f_name = file.name
                        file.close()
                        return json.dumps({"createdfile": "config"})
                except Exception as e:
                    logging.log_warning(
                        'Not found.{}'.format(e),
                        os.path.abspath(__file__),
                        sys._getframe().f_lineno
                        )
                    return None
        return None

    def get(self, name):
        """Getter."""
        if self.env in self.environments:
            try:
                with open(self.full_path) as file:
                    config = json.load(file)
                    file.close()
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
        return None
