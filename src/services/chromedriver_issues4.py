
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def setup_webdriver(dest_dir):
    """Sets up the Selenium WebDriver with the correct Chromedriver."""
    CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"  # Adjust this to your Chromedriver location

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": dest_dir}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Create the WebDriver instance
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    # Log the Chromedriver binary path
    print(f"Using Chromedriver located at: {service.path}")
    return driver

