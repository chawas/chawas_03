import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Define a dictionary for Zimbabwean stations with their latitude and longitude
stations = {
    "Harare": {"lat": -17.8178, "lon": 31.0447},
    "Bulawayo": {"lat": -20.1328, "lon": 28.6265},
    "Mutare": {"lat": -18.9707, "lon": 32.6709},
    "Gweru": {"lat": -19.4588, "lon": 29.8158},
    "Masvingo": {"lat": -20.0592, "lon": 30.8268},
}

# Calculate the base_time as midnight UTC for the current day
base_time = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
base_time_str = base_time.strftime("%Y%m%d%H%M")  # Format as required in the URL

# Setup Selenium WebDriver (example uses Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Iterate through stations, open URL and extract image URL
for station, coords in stations.items():
    lat = coords["lat"]
    lon = coords["lon"]

    # Construct the URL for the station
    url = (
        f"https://charts.ecmwf.int/products/opencharts_meteogram?"
        f"base_time={base_time_str}&epsgram=classical_10d&"
        f"lat={lat}&lon={lon}&station_name={station}"
    )

    # Open the URL in the browser
    driver.get(url)
    time.sleep(5)  # Wait for the page to load fully


    try:
        image = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='root']/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/img"))
        )
        print(image.get_attribute("src"))  # Print the image source URL
    except TimeoutException:
        print("Image not found within the given time.")

# Close the browser
driver.quit()
