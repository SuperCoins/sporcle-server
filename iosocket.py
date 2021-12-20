import asyncio
import websockets
import json


async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        print('[' + event['type'] + ']')
        message = {"type": "play"}
        await sendMessage(message, websocket)


async def sendMessage(message, websocket):
    await websocket.send(json.dumps(message))
    print('(sent) ', message)


async def main():
    async with websockets.serve(handler, "", 8080) as response:
        # print(str(response.sockets))
        await asyncio.Future()  # run forever



if __name__ == "__main__":
    asyncio.run(main())
