import requests
import json
from geopy.distance import distance

# Define the MapQuest API endpoint and parameters
endpoint = "http://www.mapquestapi.com/directions/v2/route"
params = {
    "key": "iGsmGj02YiVOmLrnSiUoOlLl3FOGpgwA",
    "routeType": "fastest",
    "unit": "m",
    'prefers':'highways',
    "destinationManeuverDisplay": "true",
    "fullShape": "true"
}

rides = [
{'driver': 'Alice', 'destination': 'cuncolim goa india', 'source': 'panjim goa india', 'seats': 3},
{'driver': 'Bob', 'destination': 'margao goa india', 'source': 'panzorkoni goa india' ,'seats': 2},
{'driver': 'Charlie', 'destination': 'sanguem goa india', 'source': 'fatorda goa india', 'seats': 1},
{'driver': 'David', 'destination': 'margao goa india', 'source': 'cuncolim goa india', 'seats': 4}
]
# Prompt the user to enter their start and end locations
user_start_location = 'panzorkoni goa india'
user_end_location = 'margao goa india'

    
# Send a GET request to the MapQuest API to get the user's route
params["from"] = user_start_location
params["to"] = user_end_location
response = requests.get(endpoint, params=params)

# Extract the user's route steps from the response JSON
user_route = []
for maneuver in response.json()["route"]["legs"][0]["maneuvers"]:
    location = maneuver["startPoint"]
    user_route.append(location)

matched_rides = []

for ride in rides:
# Send a GET request to the MapQuest API to get the driver's route
    driver_start_location = ride['source']
    driver_end_location = ride['destination']
    params["from"] = driver_start_location
    params["to"] = driver_end_location
    response = requests.get(endpoint, params=params)

# Extract the driver's route steps from the response JSON
    driver_route = []
    for maneuver in response.json()["route"]["legs"][0]["maneuvers"]:
        location = maneuver["startPoint"]
        driver_route.append(location)

    # Check if the user's starting location is on the driver's route or close to it within a certain radius
    user_start_location_on_route = False
    radius = 3000 # meters
    # print(user_route[0]['lat'])
    # print(user_route[0]['lng'])
    for location in driver_route:
        # print(user_route[0]['lat'],user_route[0]['lng'])
        # print(location["lat"], location["lng"])
        dist = distance((location["lat"], location["lng"]), (user_route[0]["lat"], user_route[0]["lng"])).m
        # print(dist)   
        # print('------------')

        if dist <= radius:
            user_start_location_on_route = True
            break

    user_end_location_on_route = False
    for location in driver_route:
        dist = distance((location["lat"], location["lng"]), (user_route[-1]["lat"], user_route[-1]["lng"])).m
        if dist <= radius:
            user_end_location_on_route = True
            break
    
    # Check if the user's route is going in the same direction as the driver's route
    opposite_direction = False
    if distance((driver_route[0]["lat"], driver_route[0]["lng"]), (user_route[-1]["lat"], user_route[-1]["lng"])).m <= radius:
        opposite_direction = True
    if distance((driver_route[-1]["lat"], driver_route[-1]["lng"]), (user_route[0]["lat"], user_route[0]["lng"])).m <= radius:
        opposite_direction = True


    # # Write the driver's route, user's route, and result to a file
    # filename = "routes.txt"
    # with open(filename, "w") as f:
    #     f.write("Driver's route:\n")
    #     for location in driver_route:
    #         location_string = json.dumps(location)
    #         f.write(location_string + "\n")
    #     f.write("User's route:\n")
    #     for location in user_route:
    #         location_string = json.dumps(location)
    #         f.write(location_string + "\n")
    #     f.write("User's starting location is on the driver's route or close to it within " + str(radius) + " meters: " + str(user_start_location_on_route) + "\n")
    #     f.write("User's ending location is on the driver's route or close to it within " + str(radius) + " meters: " + str(user_end_location_on_route) + "\n")
    #     f.write("User's route is going in the same direction as the driver's route: " + str(not opposite_direction) + "\n")

    #     print("Driver's route, user's route, and result saved to", filename)

    # Display the driver's route, user's route, and result on the console
    # print("Driver's route:")
    # for location in driver_route:
    #     print(location)
    # print("User's route:")
    # for location in user_route:
    #     print(location)
    # print("User's starting location is on the driver's route or close to it within", radius, "meters:", user_start_location_on_route)
    # print("User's ending location is on the driver's route or close to it within", radius, "meters:", user_end_location_on_route)
    # print("User's route is going in the same direction as the driver's route: " + str(not opposite_direction) + "\n")

    if user_start_location_on_route and user_end_location_on_route and not opposite_direction:
        # print("Match found!\n")
        matched_rides.append(ride)

# print('done rounds')
print(matched_rides)