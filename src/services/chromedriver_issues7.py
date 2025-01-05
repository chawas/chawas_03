from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os


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


# Example Usage
def run_satellite_download():
    # Define the destination directory
    dest_dir = "/home/wrf/deployed/chawas_03/wx_presentation/images"

    # Ensure the directory exists
    os.makedirs(dest_dir, exist_ok=True)

    # Initialize the WebDriver
    driver = setup_webdriver(dest_dir)

    # Perform tasks with the WebDriver
    driver.get("https://www.google.com")
    print(f"Page title: {driver.title}")
    driver.quit()


setup_webdriver(dest_dir="/home/wrf/deployed/chawas_03/wx_presentation/images")
run_satellite_download()