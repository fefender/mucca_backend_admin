import asyncio
import websockets
import json

async def hello(uri):
    data = json.dumps({"filename": "2019516_11240.log"})
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)
        re = await websocket.recv()
        print(re)
        # while re:
        #     print(re)

asyncio.get_event_loop().run_until_complete(
    hello('ws://localhost:8081'))
