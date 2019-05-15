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
# from vendor.mucca_logging.mucca_logging import logging
# from src.response.response import response

print("Started at {}".format(sys.argv[1]))

async def echo(websocket, path):
    data = await websocket.recv()
    print(data)
    dt = json.loads(data)
    fname = dt['filename']
    path = "../../logs/" + fname
    print(path)
    doc = ""
    for line in open(path):
        await websocket.send(line)
        time.sleep(0.3)
    # with open(path) as file:
    #     log = file.read()
        # print(log)
        # for i in log:
        #     print(i)
        #     # await websocket.send(log+i)
        #     time.sleep(0.1)

    # async for message in websocket:
    #     for i in ["msg1", "msg2", "msg3", "end"]:
    #         await websocket.send(message+i)
    #         time.sleep(1)

# arg = int(sys.argv[1])
# print(type(arg))
# if arg == 8081 | 8082 | 8083:
#     print("Opening on {}".format(sys.argv[1]))
#     ws = websockets.serve(echo, 'localhost', int(sys.argv[1]))
#     asyncio.get_event_loop().run_until_complete(ws)

ws = websockets.serve(echo, 'localhost', int(sys.argv[1]))
asyncio.get_event_loop().run_until_complete(ws)
asyncio.get_event_loop().run_forever()
