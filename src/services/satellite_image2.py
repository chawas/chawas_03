from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests


# Setup Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/RGB/NATURALCOLORENHNCD/SOUTHERNAFRICA/index.htm")



for attempt in range(3):  # Retry up to 3 times
    try:
        print(f"Attempt {attempt + 1}: Trying to locate the element...")
        dropdown = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//select[@id='dropdown-id']"))
        )
        print("Element located successfully.")
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt == 2:
            print("Max retries reached. Exiting.")