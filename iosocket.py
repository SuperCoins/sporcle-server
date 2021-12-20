import asyncio
import websockets


async def handler(websocket):
    async for message in websocket:
        print(message)


async def main():
    async with websockets.serve(handler, "", 8080) as response:
        print(str(response.sockets))
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
