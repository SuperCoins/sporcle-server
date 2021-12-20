import asyncio
import websockets
import json
import secrets

JOIN = {}

async def error(websocket, message):
    print('JOIN', JOIN)
    event = { "type": "error", "message": message }
    await sendMessage(event, websocket)

async def handler(websocket, path):
    event = await receiveMessage(websocket)
    assert event["type"] == "init"
    if "data" in event :
        await join(websocket, event["data"])
    else:
        await start(websocket)

async def join(websocket, join_key):
    try:
        print(JOIN)
        connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Server not found.")
        return

    connected.add(websocket)
    try:
        # Temporary - for testing.
        print("second player joined game")
        async for message in websocket:
            print("second player sent", message)

    finally:
        connected.remove(websocket)


async def start(websocket):
    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = {websocket}
    print('JOIN', JOIN)
    try:
        event = { "type": "init", "data": join_key }
        await sendMessage(event, websocket)
        await play(websocket, connected)
    except:
        print('something went wrong')

async def play(websocket, connected):
    async for message in websocket:
        event = json.loads(message)
        print('[' + event['type'] + ']')
        await sendMessage('hello', websocket)


async def sendMessage(message, websocket):
    await websocket.send(json.dumps(message))
    print('(sent) ', message)

async def receiveMessage(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    print('[' + event['type'] + '] ' + message)
    return event


async def main():
    async with websockets.serve(handler, "", 8080) as response:
        await asyncio.Future()  # run forever



if __name__ == "__main__":
    asyncio.run(main())
