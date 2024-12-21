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

# Set default download directory
dest_dir = "/home/wrf/deployed/webb-downloading/wx_presentation/images"  # Destination directory
prefs = {"download.default_directory": dest_dir}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/RGB/NATURALCOLORENHNCD/SOUTHERNAFRICA/index.htm")

try:
    # Wait for the dropdown to load
    print("Waiting for dropdown...")
    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )
    print("Dropdown found.")

    # Create Select object
    select = Select(dropdown)

    # Select the desired time
    desired_time = "22/11/24 06:00 UTC"
    select.select_by_visible_text(desired_time)
    print(f"Selected time: {desired_time}")

    # Wait for the image to update (if necessary)
    time.sleep(2)

    # Find the main image and get its `src` attribute
    print("Locating the main image...")
    image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    relative_path = image_element.get_attribute("src")
    print(f"Image src: {relative_path}")

    # Combine the base URL with the relative path
    base_url = "https://eumetview.eumetsat.int/"
    image_url = base_url + relative_path

    # Download the image using requests
    print("Downloading the image...")
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # Save the image to the destination directory
        file_name = os.path.join(dest_dir, "downloaded_image.jpg")
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image successfully downloaded: {file_name}")
    else:
        print(f"Failed to download image. HTTP status code: {response.status_code}")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
