import datetime


# # Dictionary of weather stations with detailed information



stations = {
    "BeitBridge": {
        "code": "67991",
        "latitude": -20.516,
        "longitude": 28.443,
        "altitude": 1670  # altitude in meters
    },
    "Bindura": {
        "code": "67",
        "latitude": -17.330,
        "longitude": 31.305,
        "altitude": 50
    },
    "Kisumu": {
        "code": "KQKIS",
        "latitude": -0.091702,
        "longitude": 34.7680,
        "altitude": 1131
    },
    "Eldoret": {
        "code": "KQELD",
        "latitude": 0.5143,
        "longitude": 35.2698,
        "altitude": 2133
    }
}

# Calculate the base_time as midnight UTC for the current day
base_time = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
base_time_str = base_time.strftime("%Y%m%d%H%M")  # Format as required in the URL




# Generate URLs for each station
for station, coords in stations.items():
    lat = coords["latitude"]
    lon = coords["longitude"]

    # Construct the URL for the station
    url = (
        f"https://charts.ecmwf.int/products/opencharts_meteogram?"
        f"base_time={base_time_str}&epsgram=classical_10d&"
        f"lat={lat}&lon={lon}&station_name={station}"
    )

    print(f"URL for {station}: {url}")

    # Example of accessing data for a specific station
    #station_name = "BeitBridge"
    #BeitBridge_info = stations.get(station_name)

    #print(f"Station: {station_name}")
    #print(f"Code: {BeitBridge_info['code']}")
    #print(f"Latitude: {BeitBridge_info['latitude']}")
    #print(f"Longitude: {BeitBridge_info['longitude']}")
    #print(f"Altitude: {BeitBridge_info['altitude']} meters")
