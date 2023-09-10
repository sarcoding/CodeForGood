import asyncio
import websockets
import json

async def request_traffic_data(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            request = input("Enter 'get_traffic_data' to request traffic data: ")
            if request == "get_traffic_data":
                await websocket.send(request)
                response = await websocket.recv()
                traffic_data = json.loads(response)
                print("Traffic Data:")
                print("Waiting Car Count:", traffic_data.get('waiting_car_count', 0))
                # Process other traffic data as needed
            else:
                print("Invalid request. Enter 'get_traffic_data' to request traffic data.")

if __name__ == "__main__":
    server_uri = "wss://localhost:8765"  # Replace with your server URI
    asyncio.get_event_loop().run_until_complete(request_traffic_data(server_uri))