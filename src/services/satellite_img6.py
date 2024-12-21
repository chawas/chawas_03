from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time



# Setup Selenium WebDriver
options = webdriver.ChromeOptions()

# Set default download directory
dest_dir = "/home/wrf/deployed/webb-downloading/wx_presentation/images"   # Destination directory (update this path)
#img_dir = "/home/wrf/deployed/webb-downloading/src/services/station_images"# Meteogra
#download_dir = "/path/to/your/download/directory"  # Change this to your preferred location
prefs = {"download.default_directory": dest_dir}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
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

    # Select the desired time
    desired_time = "21/11/24 06:00 UTC"
    select.select_by_visible_text(desired_time)
    print(f"Selected time: {desired_time}")

    # Wait for the dropdown action to process (if necessary)
    time.sleep(2)

    # Click the download button
    print("Locating and clicking the download button...")
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download')]"))  # Adjust XPath if necessary
    )
    download_button.click()
    print("Download initiated.")

    # Wait for the download to complete
    time.sleep(10)  # Adjust this based on file size or implement smarter checks (e.g., monitor the directory)

    print(f"File should be downloaded to: {dest_dir}")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
