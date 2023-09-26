import asyncio
import websockets
import json
import time
import pickle

async def request_traffic_data(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(request)
        time.sleep(secs=2)
        with open("/vehical_count.txt", 'r') as file:
            data = pickle.load(file)



if __name__ == "__main__":
    server_uri = "wss://localhost:8765"
    asyncio.get_event_loop().run_until_complete(request_traffic_data(server_uri))