import asyncio
import websockets

async def hello():
    uri = "ws://0.0.0.0:8765"
    async with websockets.connect(uri) as websocket:
        name = 'Marvin'

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())