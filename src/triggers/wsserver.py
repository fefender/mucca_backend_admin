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
import asyncio
import websockets
from vendor.mucca_logging.mucca_logging import logging
from src.response.response import response

async def echo(websocket, path):
    print("Echo called")
    data = await ws.recv()
    print(data)
    await websocket.send(message+i)
    # await asyncio.sleep(1)
    # async for message in websocket:
    #     for i in ["msg1", "msg2", "msg3", "end"]:
    #         await websocket.send(message+i)
    #         time.sleep(1)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

class wsserver():
    """Websocket server class."""

    def start(port):
        """Start."""
        print ("start")
        s_port = int(port)
        s_host = os.getenv('WSS_HOST')
        start_server = websockets.serve(echo, s_host, s_port)
        # asyncio.get_event_loop().run_until_complete(
        #     websockets.serve(echo, s_host, s_port)
        # )
        # asyncio.get_event_loop().run_forever()

# class wsserver():
#     """Websocket server class."""

# async def start(port):
#     """Start."""
#     print("Start ws server")
#     s_port = int(port)
#     s_host = os.getenv('WSS_HOST')
#     with websockets.serve(echo, s_host, s_port) as ws:
#         data = await ws.recv()
#     # def __init__(self, port):
#     #     self.host = os.getenv('WSS_HOST')
#     #     self.port= int(port)
#     #     self.start_server = websockets.serve(echo, self.host, self.port)
#     #     print("Init wsserver")
#
#     # async def hello_world(self):
#     #     while True:
#     #         print("Hello World!")
#     #         await asyncio.sleep(1)
#     #     return self
#     #
#     # def __await__(self):
#     #     return self.hello_world().__await__()
#
# async def echo(websocket, path):
#     print("in async")
#     data = await websocket.recv()
#     print("***")
#     print(data)
#
#     await websocket.send("Sto rispondendo")
#     print("RIsposta")
#     # async for message in websocket:
#     #     for i in ["msg1", "msg2", "msg3", "end"]:
#     #         await websocket.send(message+i)
#     #         time.sleep(1)
#
#     asyncio.get_event_loop().run_until_complete(
#         self.start_server
#     )
#
# # asyncio.get_event_loop().run_until_complete(
# #     websockets.serve(echo, 'localhost', 8083)
# # )
# #
# # asyncio.get_event_loop().run_until_complete(
# #     websockets.serve(echo, 'localhost', 8082)
# # )
#
#
# asyncio.get_event_loop().run_forever()
