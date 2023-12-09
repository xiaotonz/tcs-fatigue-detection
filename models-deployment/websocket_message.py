import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket, _):
    connected_clients.add(websocket)
    while True:
        try:
            message = await websocket.recv()
            print('Message received from client:', message)
            # Handle received messages here if needed
        except websockets.exceptions.ConnectionClosed:
            connected_clients.remove(websocket)
            break

def send_message(message):
    print('Message sent')
    for client in connected_clients:
        asyncio.create_task(client.send(message))
    return 'Message sent to connected clients'

async def start_server():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever