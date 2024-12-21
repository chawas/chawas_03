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

try:
    print("Waiting for dropdown...")
    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )
    print("Dropdown found.")

    select = Select(dropdown)
    desired_time = "22/11/24 09:00 UTC"
    select.select_by_visible_text(desired_time)
    print(f"Selected time: {desired_time}")

    time.sleep(2)

    print("Locating the main image...")
    image_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "mainImage"))
    )
    relative_path = image_element.get_attribute("src")
    print(f"Image src: {relative_path}")

    image_url = relative_path

    # Extract cookies from Selenium
    selenium_cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Add headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Referer": driver.current_url,  # Refer to the current page
    }

    print("Downloading the image...")
    response = session.get(image_url, headers=headers, stream=True)
    if response.status_code == 200:
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
