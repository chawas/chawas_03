import os
import requests
import shutil
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import logging


# Station Metadata
# stations = {
#     "Harare": {"latitude": -17.833, "longitude": 31.034},
#     "Bulawayo": {"latitude": -20.164, "longitude": 28.626},
#     "Gweru": {"latitude": -19.462, "longitude": 29.818},
#     "Masvingo": {"latitude": -20.085, "longitude": 30.827},
#     "Bindura": {"latitude": -17.330, "longitude": 31.305},
# }
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
        "altitude": 1310
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
        "altitude": 1130
    },

    "Chivhu": {
        "code": "67889",
        "latitude": -19.021,
        "longitude": 30.897,
        "altitude": 1465
    },
    "Gokwe": {
        "code": "67861",
        "latitude": -18.204,
        "longitude": 28.934,
        "altitude": 1180
    },
    "Gweru": {
        "code": "67867",
        "latitude": -19.462,
        "longitude": 29.818,
        "altitude": 1400
    },
    "Harare": {
        "code": "67774",
        "latitude": -17.833,
        "longitude": 31.034,
        "altitude": 1.470
    },
    "Masvingo": {
        "code": "67975",
        "latitude": -20.085,
        "longitude": 30.827,
        "altitude": 1090
    }
}



# Logging Configuration
LOG_FILE = "/home/wrf/deployed/chawas_03/wx_presentation/satellite_download.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(console_handler)





# Constants
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
MAX_RETRIES = 3
RETRY_DELAY = 60  # seconds

# def setup_webdriver(dest_dir):
#     """Sets up the Selenium WebDriver with the correct Chromedriver."""
#     if not os.path.exists(CHROMEDRIVER_PATH):
#         logging.error(f"Chromedriver not found at {CHROMEDRIVER_PATH}")
#         raise FileNotFoundError(f"Chromedriver not found at {CHROMEDRIVER_PATH}")
#
#     options = webdriver.ChromeOptions()
#     prefs = {"download.default_directory": dest_dir}
#     options.add_experimental_option("prefs", prefs)
#     options.add_argument("--headless")  # Run in headless mode
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#
#     service = Service(CHROMEDRIVER_PATH)
#     logging.info(f"Initializing WebDriver with Chromedriver located at: {CHROMEDRIVER_PATH}")
#     driver = webdriver.Chrome(service=service, options=options)
#     logging.info(f"WebDriver initialized successfully. Download directory: {dest_dir}")
#     return driver


def setup_webdriver(dest_dir):
    """Sets up the Selenium WebDriver with the correct Chromedriver."""
    if not os.path.exists(CHROMEDRIVER_PATH):
        logging.error(f"Chromedriver not found at {CHROMEDRIVER_PATH}")
        raise FileNotFoundError(f"Chromedriver not found at {CHROMEDRIVER_PATH}")

    try:
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": dest_dir}
        options.add_experimental_option("prefs", prefs)

        # Remove the '--headless' argument to make the browser visible
        # options.add_argument("--headless")  # Comment this line out
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(CHROMEDRIVER_PATH)
        logging.info(f"Initializing WebDriver with Chromedriver located at: {CHROMEDRIVER_PATH}")
        driver = webdriver.Chrome(service=service, options=options)
        logging.info(f"WebDriver initialized successfully. Download directory: {dest_dir}")
        return driver
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        raise  # Reraise the exception so the caller can handle it


def download_eps_images():
    """
    Download EPS images for the configured stations.
    """
    base_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    base_time_str = base_time.strftime("%Y%m%d%H%M")
    print(f"Base time: {base_time_str}")

    # Initialize WebDriver
    img_dir = "/path/to/download/directory"  # Update this with your path
    driver = None  # Initialize as None to handle cases where setup_webdriver fails

    urllist = []

    try:
        # Try to initialize the WebDriver
        driver = setup_webdriver(img_dir)  # Initialize the WebDriver
        if driver is None:
            logging.error("WebDriver initialization failed.")
            return urllist  # Exit early if WebDriver initialization failed

        for station, coords in stations.items():
            latitude = coords["latitude"]
            longitude = coords["longitude"]
            url = (
                f"https://charts.ecmwf.int/products/opencharts_meteogram?"
                f"base_time={base_time_str}&epsgram=classical_10d&"
                f"lat={latitude}&lon={longitude}&station_name={station}"
            )

            logging.info(f"Navigating to URL: {url}")
            driver.get(url)
            sleep(5)

            try:
                image = WebDriverWait(driver, 50).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//*[@id='root']/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/img")
                    )
                )
                image_url = image.get_attribute("src")
                print(f"Retrieved URL for {station}: {image_url}")
                urllist.append((station, image_url))
            except TimeoutException:
                logging.warning(f"Timeout: Could not retrieve image for {station}.")

    except Exception as e:
        logging.error(f"Error during EPS download: {e}")

    finally:
        # Ensure WebDriver is properly closed only if it was successfully initialized
        if driver:
            driver.quit()  # Ensure WebDriver is properly closed
        else:
            logging.error("Driver was not initialized, skipping quit.")

    # Save URLs to a config file
    save_image_urls(urllist, "../config2.py")
    return urllist



# def download_eps_images():
#     """
#     Download EPS images for the configured stations.
#     """
#     base_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#     base_time_str = base_time.strftime("%Y%m%d%H%M")
#     print(f"Base time: {base_time_str}")
#
#     #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     urllist = []
#
#     try:
#         for station, coords in stations.items():
#             latitude = coords["latitude"]
#             longitude = coords["longitude"]
#             url = (
#                 f"https://charts.ecmwf.int/products/opencharts_meteogram?"
#                 f"base_time={base_time_str}&epsgram=classical_10d&"
#                 f"lat={latitude}&lon={longitude}&station_name={station}"
#             )
#
#             driver.get(url)
#             sleep(5)
#
#             try:
#                 image = WebDriverWait(driver, 50).until(
#                     EC.visibility_of_element_located(
#                         (By.XPATH, "//*[@id='root']/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/img")
#                     )
#                 )
#                 image_url = image.get_attribute("src")
#                 print(f"Retrieved URL for {station}: {image_url}")
#                 urllist.append((station, image_url))
#             except TimeoutException:
#                 print(f"Timeout: Could not retrieve image for {station}.")
#
#     finally:
#         driver.quit()
#
#     # Save URLs to a config file
#     save_image_urls(urllist, "config2.py")
#     return urllist


def save_image_urls(urllist, config_file_path):
    """
    Save the list of image URLs to a configuration file.
    """
    try:
        with open(config_file_path, "w") as config_file:
            config_file.write(f"urllist = {urllist}\n")
        print(f"Image URLs saved to {config_file_path}")
    except Exception as e:
        print(f"Error saving image URLs: {e}")


def download_station_images(urllist, dest_dir):
    """
    Download images for each station and save them in the destination directory.
    """
    os.makedirs(dest_dir, exist_ok=True)

    for station, url in urllist:
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_path = os.path.join(dest_dir, f"{station}.png")
            with open(image_path, "wb") as image_file:
                image_file.write(response.content)
            print(f"Downloaded and saved image for {station}: {image_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image for {station}: {e}")


def copy_eps_to_images_folder(source_dir, dest_dir):
    """
    Copy EPS images from the source directory to the destination directory.
    """
    if not os.path.isdir(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return

    try:
        for item in os.listdir(source_dir):
            src_path = os.path.join(source_dir, item)
            dest_path = os.path.join(dest_dir, item)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dest_path)
                print(f"Copied file: {src_path} to {dest_path}")
            elif os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                print(f"Copied directory: {src_path} to {dest_path}")
        print(f"Finished copying contents of {source_dir} to {dest_dir}")
    except Exception as e:
        print(f"Error copying files: {e}")


def run_eps_download():
    """
    Run the full EPS download process: fetch URLs, download images, and copy files.
    """
    img_dir = "/home/wrf/deployed/webb-downloading/src/services/station_images"
    dest_dir = "/home/wrf/deployed/webb-downloading/wx_presentation/images"
    urllist = download_eps_images()
    download_station_images(urllist, img_dir)
    copy_eps_to_images_folder(img_dir, dest_dir)


if __name__ == "__main__":
    run_eps_download()
