from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Setup Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/RGB/NATURALCOLORENHNCD/SOUTHERNAFRICA/index.htm")

try:
    # Wait for the dropdown to be present
    print("Waiting for dropdown...")
    dropdown = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.NAME, "selectImage"))
    )
    print("Dropdown found.")

    # Create a Select object to interact with the dropdown
    select = Select(dropdown)

    # Select the option with visible text "21/11/24 06:00 UTC"
    desired_time = "21/11/24   06:00 UTC"  # Update to match the format in the dropdown
    select.select_by_visible_text(desired_time)
    print(f"Selected time: {desired_time}")

    # Optional: Wait for the page or data to update
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img"))
    )
    print("Page updated for the selected time.")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
