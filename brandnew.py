import requests
import json
from geopy.distance import distance

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

endpoint = "http://www.mapquestapi.com/directions/v2/route"
params = {
    "key": "iGsmGj02YiVOmLrnSiUoOlLl3FOGpgwA",
    "routeType": "fastest",
    "unit": "m",
    'prefers':'highways',
    "destinationManeuverDisplay": "true",
    "fullShape": "true"
}

user_start_location = 'panzorkoni goa india'
user_end_location = 'margao goa india'

params["from"] = user_start_location
params["to"] = user_end_location
response = requests.get(endpoint, params=params)

user_route = []
for maneuver in response.json()["route"]["legs"][0]["maneuvers"]:
    location = maneuver["startPoint"]
    user_route.append(location)

matched_rides = []
cred = credentials.Certificate('b.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
rides_ref = db.collection('rides')

rides = rides_ref.where('ride_status', '==', 'active').get()

for ride in rides:
    ride_data = ride.to_dict()
    # print(ride_data)
    print('----------------')
    driver_start_location = ride_data['start_loc']
    driver_end_location = ride_data['end_loc']
    params["from"] = driver_start_location
    params["to"] = driver_end_location

    response = requests.get(endpoint, params=params)
    # print(response)

    driver_route = []
    for maneuver in response.json()["route"]["legs"][0]["maneuvers"]:
        location = maneuver["startPoint"]
        driver_route.append(location)
    # print(driver_route)
    user_start_location_on_route = False
    radius = 3000 # meters
    for location in driver_route:   
        dist = distance((location["lat"], location["lng"]), (user_route[0]["lat"], user_route[0]["lng"])).m
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

    if user_start_location_on_route and user_end_location_on_route and not opposite_direction:
        # print("Match found!\n")
        matched_rides.append(ride_data)

print(matched_rides)