from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
import time
import os

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
dest_dir = "/home/wrf/deployed/webb-downloading/wx_presentation/images"
prefs = {"download.default_directory": dest_dir}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

def download_satellite_images(image_name, image_url, dest_dir, rename_to):
    """
    Download and rename an image file.
    """
    try:
        # Extract cookies from Selenium
        selenium_cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Add headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
            "Referer": driver.current_url,
        }

        print(f"Downloading {image_name}...")
        response = session.get(image_url, headers=headers, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(dest_dir, rename_to)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"{image_name} successfully downloaded and saved as: {file_path}")
        else:
            print(f"Failed to download {image_name}. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {image_name}: {e}")


try:
    # Define desired times for each image type
    desired_times = {
        "natural_colour": "24/11/24 06:00 UTC",
        "natural_colour2": "23/11/24 06:00 UTC",
        "infra_radiation": "24/11/24 06:00 UTC",
        "infra_radiation2": "23/11/24 06:00 UTC",
        "water_vapour": "24/11/24 00:00 UTC",
        "water_vapour2": "23/11/24 00:00 UTC"
    }

    # Natural Color Image Today
    print("Loading Natural Color Image Today page...")
    driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/RGB/NATURALCOLORENHNCD/SOUTHERNAFRICA/index.htm")

    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )

    select = Select(dropdown)
    print("i managed ...")
    natural_time = desired_times["natural_colour"]
    select.select_by_visible_text(natural_time)
    print(f"Selected time for Natural Colour Today: {natural_time}")
    time.sleep(5)
    natural_image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    natural_image_url = natural_image_element.get_attribute("src")
    download_satellite_images("Natural Colour Image Today", natural_image_url, dest_dir, "natural_colour_today.jpg")


    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )
    select = Select(dropdown)
    natural_time = desired_times["natural_colour2"]
    select.select_by_visible_text(natural_time)
    print(f"Selected time for Natural Colour Yesterday: {natural_time}")
    time.sleep(5)
    natural_image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    natural_image_url = natural_image_element.get_attribute("src")
    download_satellite_images("Natural Colour Image Yesterday", natural_image_url, dest_dir, "natural_colour_yesterday.jpg")

    # Infra-radiation Image
    print("Loading Infra-radiation today page...")
    driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/IMAGERY/IR108/BW/SOUTHERNAFRICA/index.htm")

    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )
    select = Select(dropdown)
    infra_time = desired_times["infra_radiation"]
    select.select_by_visible_text(infra_time)
    print(f"Selected time for Infra-radiation today: {infra_time}")
    time.sleep(2)
    infra_image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    infra_image_url = infra_image_element.get_attribute("src")
    download_satellite_images("Infra-radiation Image Today", infra_image_url, dest_dir, "infra_radiation_today.jpg")


    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )
    select = Select(dropdown)
    infra_time = desired_times["infra_radiation2"]
    select.select_by_visible_text(infra_time)
    print(f"Selected time for Infra-radiation Yesterday: {infra_time}")
    time.sleep(2)
    infra_image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    infra_image_url = infra_image_element.get_attribute("src")
    download_satellite_images("Infra-radiation Image Yesterday", infra_image_url, dest_dir, "infra_radiation_yesterday.jpg")

    # Water Vapour Image
    print("Loading Water Vapour Today page...")
    driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/IMAGERY/WV062/BW/SOUTHERNAFRICA/index.htm")

    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )
    select = Select(dropdown)
    water_vapour_time = desired_times["water_vapour"]
    select.select_by_visible_text(water_vapour_time)
    print(f"Selected time for Water Vapour Today: {water_vapour_time}")
    time.sleep(2)
    water_vapour_image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    water_vapour_image_url = water_vapour_image_element.get_attribute("src")
    download_satellite_images("Water Vapour Image Today", water_vapour_image_url, dest_dir, "water_vapour_today.jpg")

    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )
    select = Select(dropdown)
    water_vapour_time = desired_times["water_vapour2"]
    select.select_by_visible_text(water_vapour_time)
    print(f"Selected time for Water Vapour Yesterday: {water_vapour_time}")
    time.sleep(2)
    water_vapour_image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    water_vapour_image_url = water_vapour_image_element.get_attribute("src")
    download_satellite_images("Water Vapour Image Yesterday", water_vapour_image_url, dest_dir, "water_vapour_yesterday.jpg")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
