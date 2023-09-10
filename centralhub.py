import asyncio
import websockets
import json

default_total_signal_time = 240
default_single_road_time = 60

vehicle_counts = {
    'road1': 10,
    'road2': 8,
    'road3': 5,
    'road4': 18 
}


def manage(counts):
    total_vehicles_road1 = vehicle_counts['road1']
    total_vehicles_road2 = vehicle_counts['road2']
    total_vehicles_road3 = vehicle_counts['road3']
    total_vehicles_road4 = vehicle_counts['road4']

    signal_time_road1 = default_single_road_time * total_vehicles_road1 / (sum(vehicle_counts.values()))
    signal_time_road2 = default_single_road_time * total_vehicles_road2 / (sum(vehicle_counts.values()))
    signal_time_road3 = default_single_road_time * total_vehicles_road3 / (sum(vehicle_counts.values()))
    signal_time_road4 = default_single_road_time * total_vehicles_road4 / (sum(vehicle_counts.values()))

    actual_total_signal_time = signal_time_road1 + signal_time_road2 + signal_time_road3 + signal_time_road4

    adjustment = default_total_signal_time - actual_total_signal_time

    # Adjust signal times for both roads
    signal_time_road2 += adjustment / 4
    signal_time_road1 += adjustment / 4
    signal_time_road3 += adjustment / 4
    signal_time_road4 += adjustment / 4

    signal_time_road1 = max(10, min(120, signal_time_road1))
    signal_time_road2 = max(10, min(120, signal_time_road2))
    signal_time_road3 = max(10, min(120, signal_time_road3))
    signal_time_road4 = max(10, min(120, signal_time_road4))

    print(f"Green signal for road 1: {signal_time_road1:.2f} seconds")
    print(f"Green signal for road 2: {signal_time_road2:.2f} seconds")
    print(f"Green signal for road 3: {signal_time_road3:.2f} seconds")
    print(f"Green signal for road 4: {signal_time_road4:.2f} seconds")

async def request_traffic_data(uri):
    async with websockets.connect(uri) as websocket:
        while True:

            response = await websocket.recv()
            traffic_data = json.loads(response)
            print("Traffic Data:")
            print("Waiting Car Count:", traffic_data.get('waiting_car_count', 0))

if __name__ == "__main__":
    server_uri = "ws://localhost:8765"  # Replace with your server URI
    asyncio.get_event_loop().run_until_complete(request_traffic_data(server_uri))



manage(vehicle_counts)
