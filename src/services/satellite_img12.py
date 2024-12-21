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
driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/RGB/NATURALCOLORENHNCD/SOUTHERNAFRICA/index.htm")


def download_image(image_name, image_url, dest_dir, rename_to):
    """
    Download and rename an image file.
    :param image_name: Name of the image (for logging purposes)
    :param image_url: URL of the image
    :param dest_dir: Directory to save the image
    :param rename_to: New file name after downloading
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







# Define a dictionary for desired times for each image type
desired_times = {
    "natural_color": "24/11/24 06:00 UTC",
    "natural_color2": "24/11/24 06:00 UTC",
    "infra_radiation": "24/11/24 06:00 UTC",
    "infra_radiation2": "24/11/24 06:00 UTC",
    "water_vapour": "23/11/24 00:00 UTC",
    "water_vapour2": "23/11/24 00:00 UTC"
}


try:
    # Waiting for dropdown to load
    print("Waiting for dropdown...")
    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )
    print("Dropdown found.")

    # Create a Select object for the dropdown
    select = Select(dropdown)

    # Download Natural Color Image
    natural_time = desired_times["natural_color"]
    select.select_by_visible_text(natural_time)
    print(f"Selected time for Natural Color: {natural_time}")
    time.sleep(2)  # Allow the page to update

    natural_image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    natural_image_url = natural_image_element.get_attribute("src")
    download_image("Natural Color Image", natural_image_url, dest_dir, "natural_color.jpg")

    # Switch to Infra-radiation image (example logic: replace URL pattern or switch tab if applicable)
    print("Switching to Infra-radiation image...")
    driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/IMAGERY/IR108/BW/SOUTHERNAFRICA/index.htm")  # Adjust this URL if necessary

    infra_time = desired_times["infra_radiation"]
    select.select_by_visible_text(infra_time)
    print(f"Selected time for Infra-radiation: {infra_time}")
    time.sleep(2)  # Allow the page to update again

    # Re-locate the mainImage element for Infra-radiation
    infra_image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    infra_image_url = infra_image_element.get_attribute("src")
    download_image("Infra-radiation Image", infra_image_url, dest_dir, "infra_radiation.jpg")

    # Download Water Vapour Image
    # Switch to Water Vapour image (example logic: replace URL pattern or switch tab if applicable)
    print("Switching to Water Vapour image...")
    driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/IMAGERY/WV062/BW/SOUTHERNAFRICA/index.htm")  # Adjust this URL if necessary

    water_vapour_time = desired_times["water_vapour"]
    select.select_by_visible_text(water_vapour_time)
    print(f"Selected time for Water Vapour: {water_vapour_time}")
    time.sleep(2)

    # Re-locate the mainImage element for Water Vapour
    water_vapour_image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    water_vapour_image_url = water_vapour_image_element.get_attribute("src")
    download_image("Water Vapour Image", water_vapour_image_url, dest_dir, "water_vapour.jpg")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
