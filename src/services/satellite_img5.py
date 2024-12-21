from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Setup Selenium WebDriver
driver = webdriver.Chrome()
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

    # Debug: Print all available options
    options = [option.text for option in select.options]
    print("Available options:", options)

    # Correct the desired_time string to match the format in options
    desired_time = "21/11/24 06:00 UTC"  # Adjusted to match the exact dropdown text
    if desired_time in options:
        select.select_by_visible_text(desired_time)
        print(f"Selected time: {desired_time}")
    else:
        print(f"Desired time '{desired_time}' not found in dropdown options.")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
