import os, sys
import time
import json
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests

from config import CHROMEDRIVER_PATH, MAX_RETRIES, DELAY_SECONDS, BASE_DIR, SRC_DIR
# Use CHROMEDRIVER_PATH and other configurations
print(f"Using Chromedriver at: {CHROMEDRIVER_PATH}")
print(f"Retries allowed: {MAX_RETRIES}, Delay between retries: {DELAY_SECONDS}s")

# Where are configuration files
CONFIG_PATH = os.path.join(SRC_DIR, "config.json")
print(f"CONFIG_PATH from config: {CONFIG_PATH}")

# Check variables
print(f"BASE_DIR: {BASE_DIR}")
print(f"CONFIG_PATH: {CONFIG_PATH}")

# Load configuration
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as config_file:
    CONFIG = json.load(config_file)

# Retrieve base_dir or other configuration values
try:
#    BASE_DIR = CONFIG.get("base_dir", BASE_DIR)  # Use existing BASE_DIR as a fallback
#   SRC_DIR = os.path.join(BASE_DIR, "src")
    print(f"BASE_DIR from config: {BASE_DIR}")
    print(f"SRC_DIR: {SRC_DIR}")
except KeyError as e:
    raise KeyError(f"Key missing in {CONFIG_PATH}: {e}. Config content: {json.dumps(CONFIG, indent=4)}")


# Constants from Config
print(json.dumps(CONFIG, indent=4))



# Debugging output
if not os.path.exists(CHROMEDRIVER_PATH):
    raise FileNotFoundError(f"Chromedriver not found at {CHROMEDRIVER_PATH}")
print(f"Chromedriver path: {CHROMEDRIVER_PATH}")
LOG_FILE = os.path.join(BASE_DIR, "wx_presentation", "satellite_download.log")
#CHROMEDRIVER_PATH = CONFIG["chromedriver_path"]
DEST_DIR = os.path.join(BASE_DIR, "wx_presentation", "images")
#MAX_RETRIES = CONFIG["max_retries"]
RETRY_DELAY = CONFIG["retry_config"]["delay_seconds"]

# Logging Configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)

# Helper Functions
def calculate_time_taken(start_time):
    """Calculate the time taken for the script to run."""
    elapsed_time = time.time() - start_time
    return f"Time taken: {elapsed_time:.2f} seconds"

def setup_webdriver(dest_dir):
    """Set up Selenium WebDriver."""
    if not os.path.exists(CHROMEDRIVER_PATH):
        logging.error(f"Chromedriver not found at {CHROMEDRIVER_PATH}")
        raise FileNotFoundError(f"Chromedriver not found at {CHROMEDRIVER_PATH}")

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": dest_dir}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(CHROMEDRIVER_PATH)
    logging.info(f"Initializing WebDriver with Chromedriver located at: {CHROMEDRIVER_PATH}")
    driver = webdriver.Chrome(service=service, options=options)
    logging.info(f"WebDriver initialized successfully. Download directory: {dest_dir}")
    return driver

def generate_desired_times():
    """Generate desired times dictionary."""
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)

    today_str = today.strftime("%d/%m/%y")
    yesterday_str = yesterday.strftime("%d/%m/%y")

    return {
        "natural_colour": f"{today_str} 06:00 UTC",
        "natural_colour2": f"{yesterday_str} 06:00 UTC",
        "infra_radiation": f"{today_str} 06:00 UTC",
        "infra_radiation2": f"{yesterday_str} 06:00 UTC",
        "water_vapour": f"{today_str} 00:00 UTC",
        "water_vapour2": f"{yesterday_str} 00:00 UTC",
    }

def download_image(image_name, image_url, dest_dir, rename_to):
    """Download and rename an image."""
    try:
        logging.info(f"Downloading {image_name}...")
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(dest_dir, rename_to)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            logging.info(f"{image_name} successfully downloaded as {file_path}.")
        else:
            logging.warning(f"Failed to download {image_name}. HTTP status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error downloading {image_name}: {e}")

def download_satellite_images(driver, desired_times, dest_dir):
    """Download configured satellite images."""
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
        logging.info(f"Loading page: {page['page_url']}")
        driver.get(page["page_url"])
        dropdown = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.NAME, "selectImage")))
        select = Select(dropdown)

        for image in page["images"]:
            time_key = image["time_key"]
            rename_to = image["rename_to"]

            if time_key not in desired_times:
                logging.warning(f"Time key '{time_key}' not found in desired_times. Skipping.")
                continue

            time_value = desired_times[time_key]
            select.select_by_visible_text(time_value)
            logging.info(f"Selected time: {time_value} for {rename_to}")
            time.sleep(5)

            image_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "mainImage")))
            image_url = image_element.get_attribute("src")
            download_image(f"{time_key} Image", image_url, dest_dir, rename_to)

def run_satellite_download():
    """Run satellite image download with retries."""
    os.makedirs(DEST_DIR, exist_ok=True)
    desired_times = generate_desired_times()
    logging.info(f"Generated desired_times: {desired_times}")

    retries = 0
    start_time = time.time()

    while retries < MAX_RETRIES:
        try:
            driver = setup_webdriver(DEST_DIR)
            download_satellite_images(driver, desired_times, DEST_DIR)
            driver.quit()
            logging.info(f"Download process completed. {calculate_time_taken(start_time)}")
            return
        except Exception as e:
            retries += 1
            logging.error(f"Attempt {retries} failed: {e}")
            if retries < MAX_RETRIES:
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logging.error("Max retries reached. Download process failed.")
                break

if __name__ == "__main__":
    logging.info("Script started.")
    run_satellite_download()
    logging.info("Script ended.")
