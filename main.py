import asyncio
import json
import logging
import websockets


logging.basicConfig()

USERS = []


async def notify_users(message):
    if USERS:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user["websocket"].send(message) for user in USERS])


async def register(websocket, user):
    USERS.append({"websocket":websocket,"user":user})
    message = {
        "message":f"User {user} joined the chat.",
        "type": "register",
        "user": user
    }
    print(message, websocket)
    await notify_users(json.dumps(message))


async def unregister(websocket, user):
    USERS.remove({"websocket":websocket,"user":user})
    message = {
        "message":f"User {user} left the chat.",
        "type": "unregister",
        "user": user
    }
    print(message)
    await notify_users(json.dumps(message))


async def counter(websocket, path):
    user = path[1:]
    # register(websocket) sends user_event() to websocket
    await register(websocket, user)
    try:
        #await websocket.send(state_event())
        async for message in websocket:
            message_json = json.loads(message)
            message_json["user"] = user
            await notify_users(json.dumps(message_json))
    finally:
        await unregister(websocket, user)


if __name__ == '__main__':
    start_server = websockets.serve(counter, None, 6789)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()