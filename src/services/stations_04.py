import datetime
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Define a dictionary for Zimbabwean stations with their latitude and longitude
# stations = {
#     "Harare": {"lat": -17.8178, "lon": 31.0447},
#     "Bulawayo": {"lat": -20.1328, "lon": 28.6265},
#     "Mutare": {"lat": -18.9707, "lon": 32.6709},
#     "Gweru": {"lat": -19.4588, "lon": 29.8158},
#     "Masvingo": {"lat": -20.0592, "lon": 30.8268},
# }



#
# Dorowa;-19.055;31.775
# Gokwe;-18.217;28.943
# Gonarezhou;-21.800;31.717
# GreatZimbabwe;-20.267;30.933
# Gutu;-19.62;31.270
# Gwanda;-20.958;28.996
# Gweru;-19.462;29.818
# Harare;-17.833;31.034
# HotSprings;-19.650;32.467
# Hwange;-18.350;26.500
# HwangeNatPark;-19.117;26.600
# Insiza;-19.783;29.192
# Kadoma;-18.361;29.915
# Kanyemba;-15.627;30.419
# Kariba;-16.519;28.851
# Karoi;-16.818;29.691
# Kwekwe;-18.968;29.830
# Lupane;-18.941;27.771
# Mangwe;-20.700;28.067
# Marondera;-18.252;31.526
# Masvingo;-20.085;30.827
# Matobo;-20.516;28.443
# Mazowe;-17.500;30.967
# Mberengwa;-20.7798;30.219
# MtDarwin;-16.771;31.579
# Murambinda;-19.276;31.647
# Mutare;-18.975;32.664
# Nyanga;-18.221;32.741
# Rusape;-18.536;32.132
# Umzingwane;-20.283;28.950
# VicFalls;-17.926;25.852
# Vumba;-19.084;32.752
# WestNicholson;-21.060;29.361
#
#
#
#
#
#
# Chivhu;-19.021;30.897

stations = {
    "Beitbridge": {
        "code": "67991",
        "latitude": -20.516,
        "longitude": 28.443,
        "altitude": 460  # altitude in meters
    },
    "Bindura": {
            "code": "67XXX",
            "latitude": -17.330,
            "longitude": 31.305,
            "altitude": 1130
        },
    "Binga": {
            "code": "67755",
            "latitude": -17.626,
            "longitude": 27.340,
            "altitude": 650
        },
    "Birchenough Bridge": {
            "code": "67XXX",
            "latitude": -17.626,
            "longitude": 27.340,
            "altitude": 650
        },
        
     "Buhera": {
           "code": "67785",
            "latitude": -19.312,
            "longitude": 31.433,
            "altitude": 1000
        },

     "Bulawayo": {
            "code": "67964",
            "latitude": -20.164,
            "longitude": 28.626,
            "altitude": 1340
        },
     "Chimanimani": {
            "code": "67XXX",
            "latitude": -17.330,
            "longitude": 31.305,
            "altitude": 50
        },
     "Chinhoyi": {
            "code": "67771",
            "latitude": -17.367,
            "longitude": 30.200,
            "altitude": 1170
        },
     "Chipinge": {
            "code": "67889",
            "latitude": -20.183,
            "longitude": 32.617,
            "altitude": 0000
        }


}


# Calculate the base_time as midnight UTC for the current day
base_time = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
base_time_str = base_time.strftime("%Y%m%d%H%M")  # Format as required in the URL

# Setup Selenium WebDriver (example uses Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Initialize an empty list for image URLs
urllist = []

# Iterate through stations, open URL, and extract image URL
for station, coords in stations.items():
    latitude = coords["latitude"]
    longitude = coords["longitude"]

    # Construct the URL for the station
    url = (
        f"https://charts.ecmwf.int/products/opencharts_meteogram?"
        f"base_time={base_time_str}&epsgram=classical_10d&"
        f"lat={latitude}&lon={longitude}&station_name={station}"
    )

    # Open the URL in the browser
    driver.get(url)
    time.sleep(5)  # Wait for the page to load fully

    try:
        # Locate the image and get its source URL
        image = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='root']/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/img"))
        )
        image_url = image.get_attribute("src")
        print(f"Retrieved URL for {station}: {image_url}")

        # Add the station and image URL as a tuple to urllist
        urllist.append((station, image_url))

    except TimeoutException:
        print(f"Image not found within the given time for {station}.")

# Close the browser
driver.quit()

# Save urllist to config2.py
with open("config2.py", "w") as config_file:
    config_file.write(f"urllist = {urllist}\n")

print("Image URLs saved to config2.py as urllist.")

# Step 2: Download each image and save with station name
# Create a directory for the images if it doesn't already exist
os.makedirs("station_images", exist_ok=True)

for station, url in urllist:
    try:
        # Send a request to download the image
        response = requests.get(url)
        response.raise_for_status()  # Check if the download was successful

        # Save the image with the station name
        image_path = os.path.join("station_images", f"{station}.png")
        with open(image_path, "wb") as image_file:
            image_file.write(response.content)

        print(f"Downloaded and saved image for {station} as {station}.png")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download image for {station}: {e}")
