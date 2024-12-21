from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests

# Setup Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/RGB/NATURALCOLORENHNCD/SOUTHERNAFRICA/index.htm")

try:
    # Wait for the dropdown element to be visible
    dropdown = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@id, 'dropdown-id')]"))
    )

    # Wait for the specific option text to be present
    option = WebDriverWait(driver, 100).until(
        EC.text_to_be_present_in_element((By.XPATH, "//select[contains(@id, 'dropdown-id')]/option"),
                                         "21/11/24   06:00 UTC")
    )

    # Wait for the image to update
    image_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//img"))  # Replace with the actual XPath of the image element
    )

    # Get the image URL
    image_url = image_element.get_attribute("src")
    print(f"Image URL: {image_url}")

    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        filename = "natural_color_0600Z.png"
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Image downloaded successfully as {filename}")
    else:
        print("Failed to download the image.")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
