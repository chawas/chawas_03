from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
import time
import os
from datetime import datetime, timedelta





# def setup_webdriver(dest_dir):
# #     """
# #     Initialize the Selenium WebDriver with the required settings.
# #     """
#      options = webdriver.ChromeOptions()
#      prefs = {"download.default_directory": dest_dir}
#      options.add_experimental_option("prefs", prefs)
#      return webdriver.Chrome(options=options)



# def setup_webdriver(dest_dir):
#     options = webdriver.ChromeOptions()
#     options.binary_location = "/usr/bin/"  # Specify the correct Chrome binary path
#     prefs = {"download.default_directory": dest_dir}
#     options.add_experimental_option("prefs", prefs)
#     driver = webdriver.Chrome(options=options)
#     options.add_argument("--headless=new")  # Use --headless=new for modern headless mode
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#
#     print(f"Using Chrome binary at: {options.binary_location}")
#     print(f"Using Chromedriver at: {webdriver.Chrome.__file__}")
#
#     return driver


def setup_webdriver(dest_dir):
    """Sets up the Selenium WebDriver with the correct Chromedriver."""
    CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"  # Path to Chromedriver binary

    if not os.path.exists(CHROMEDRIVER_PATH):
        raise FileNotFoundError(f"Chromedriver not found at {CHROMEDRIVER_PATH}")

    print(f"Initializing WebDriver with Chromedriver located at: {CHROMEDRIVER_PATH}")

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": dest_dir}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Initialize the Selenium WebDriver
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    print(f"WebDriver initialized successfully with downloads directed to: {dest_dir}")
    return driver


def generate_desired_times():
    """
    Generate the desired_times dictionary with today's and yesterday's dates and times.
    """
    # Get today's date and yesterday's date
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)

    # Format times as required (e.g., "24/11/24 06:00 UTC")
    today_str = today.strftime("%d/%m/%y")
    yesterday_str = yesterday.strftime("%d/%m/%y")

    desired_times = {
        "natural_colour": f"{today_str} 06:00 UTC",
        "natural_colour2": f"{yesterday_str} 06:00 UTC",
        "infra_radiation": f"{today_str} 06:00 UTC",
        "infra_radiation2": f"{yesterday_str} 06:00 UTC",
        "water_vapour": f"{today_str} 00:00 UTC",
        "water_vapour2": f"{yesterday_str} 00:00 UTC"
    }

    return desired_times


def download_image(image_name, image_url, dest_dir, rename_to):
    """
    Download and rename an image file.
    """
    try:
        print(f"Downloading {image_name}...")
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(dest_dir, rename_to)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"{image_name} successfully downloaded as {file_path}.")
        else:
            print(f"Failed to download {image_name}. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {image_name}: {e}")

def download_satellite_images(driver, desired_times, dest_dir):
    """
    Download all configured satellite images.
    """
    satellite_pages = [
        {
            "page_url": "https://eumetview.eumetsat.int/static-images/MSGIODC/RGB/NATURALCOLORENHNCD/SOUTHERNAFRICA/index.htm",
            "images": [
                {"time_key": "natural_colour", "rename_to": "natural_colour_today.jpg"},
                {"time_key": "natural_colour2", "rename_to": "natural_colour_yesterday.jpg"}
            ]
        },
        {
            "page_url": "https://eumetview.eumetsat.int/static-images/MSGIODC/IMAGERY/IR108/BW/SOUTHERNAFRICA/index.htm",
            "images": [
                {"time_key": "infra_radiation", "rename_to": "infra_radiation_today.jpg"},
                {"time_key": "infra_radiation2", "rename_to": "infra_radiation_yesterday.jpg"}
            ]
        },
        {
            "page_url": "https://eumetview.eumetsat.int/static-images/MSGIODC/IMAGERY/WV062/BW/SOUTHERNAFRICA/index.htm",
            "images": [
                {"time_key": "water_vapour", "rename_to": "water_vapour_today.jpg"},
                {"time_key": "water_vapour2", "rename_to": "water_vapour_yesterday.jpg"}
            ]
        }
    ]

    for page in satellite_pages:
        print(f"Loading page: {page['page_url']}")
        driver.get(page["page_url"])
        dropdown = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.NAME, "selectImage"))
        )
        select = Select(dropdown)

        for image in page["images"]:
            time_key = image["time_key"]
            rename_to = image["rename_to"]

            if time_key not in desired_times:
                print(f"Time key '{time_key}' not found in desired_times. Skipping.")
                continue

            time_value = desired_times[time_key]
            select.select_by_visible_text(time_value)
            print(f"Selected time: {time_value} for {rename_to}")
            time.sleep(5)  # Allow the page to update

            image_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "mainImage"))
            )
            image_url = image_element.get_attribute("src")
            download_image(f"{time_key} Image", image_url, dest_dir, rename_to)

def run_satellite_download():
    """
    Encapsulates the full satellite image download process.
    """
    dest_dir = "/home/wrf/deployed/chawas_03/wx_presentation/images"

    # Dynamically generate the desired_times dictionary
    desired_times = generate_desired_times()
    print("Generated desired_times:", desired_times)  # Debug: Print the generated times

    driver = setup_webdriver(dest_dir)
    try:
        download_satellite_images(driver, desired_times, dest_dir)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_satellite_download()
