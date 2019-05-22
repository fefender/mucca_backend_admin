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
"""Websocket server class."""
import os
import sys
import time
import json
import asyncio
import websockets
from dotenv import load_dotenv
from dotenv import find_dotenv
from importlib import import_module
import subprocess
from subprocess import Popen, PIPE
from vendor.mucca_logging.mucca_logging import logging


class wsServer():

    def __init__(self, name):
        """Class constructor."""
        self.port =  int(sys.argv[1])
        self.host = os.getenv('WSS_HOST')
        self.port_list = [8081, 8082, 8083]

    # def health_check(self, path, request_headers):
    #     print(path)
    #     print(request_headers)

    def run(self):
        """Server run."""
        # if self.host == 8081 or 8082 or 8083:
        ws = websockets.serve(
            self.handler,
            self.host,
            self.port)
        # ws = websockets.serve(
        #     self.handler,
        #     self.host,
        #     self.port,
        #     process_request=self.health_check)
        logging.log_info(
            "{} up at:{}".format(
            name, self.port),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        # print(dir(websockets))
        try:
            asyncio.get_event_loop().run_until_complete(ws)
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            logging.log_warning(
                "Wsserver already up at {}.{}".format(self.port, e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )

    async def handler(self, websocket, path):
        """Websocket handler."""
        data = await websocket.recv()
        path = self.getPath(data)
        if path is not None:
            for line in open(path):
                time.sleep(0.8)
                await websocket.send(line)
                if "Done." not in line:
                    time.sleep(0.5)


    def getPath(self, rec):
        """Get logs path."""
        data = json.loads(rec)
        try:
            fname = data['filename']
        except Exception as e:
            logging.log_error(
                "Bad request. {}".format(e),
                os.path.abspath(__file__),
                sys._getframe().f_lineno
            )
            return None
        path = "logs/" + fname
        return path

if __name__ == "__main__":
    try:
        load_dotenv(find_dotenv())
        name = os.getenv('WSS_NAME')
        app = wsServer(name)
        if app.port in app.port_list:
            app.run()
    except KeyboardInterrupt:
        logging.log_info(
            "Intercepted KeyboardInterrupt close {}".format(name),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        del app
        sys.exit()
