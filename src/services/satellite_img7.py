from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# Initialize the driver (ensure that you have the right WebDriver)
#driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
# Setup Selenium WebDriver
options = webdriver.ChromeOptions()

# Set default download directory
dest_dir = "/home/wrf/deployed/webb-downloading/wx_presentation/images"   # Destination directory (update this path)
#img_dir = "/home/wrf/deployed/webb-downloading/src/services/station_images"# Meteogra
download_dir = "/path/to/your/download/directory"  # Change this to your preferred location
prefs = {"download.default_directory": dest_dir}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.get("https://eumetview.eumetsat.int/static-images/MSGIODC/RGB/NATURALCOLORENHNCD/SOUTHERNAFRICA/index.htm")
try:
    # Navigate to the webpage
    driver.get("http://example.com")

    # Wait for the dropdown to be visible
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@id='dropdown_id']"))  # Adjust XPath to target your dropdown
    )

    # Select the desired time from the dropdown
    selected_time = "21/11/24 06:00 UTC"  # Example selection
    select = Select(dropdown)
    select.select_by_visible_text(selected_time)  # Select by visible text

    print(f"Selected time: {selected_time}")

    # Wait for the dropdown to close or update based on the selection
    time.sleep(1)  # Adjust this if necessary to ensure the page refreshes after selecting

    # Now click on the selected option (which may trigger the image load)
    option_xpath = f"//option[text()='{selected_time}']"
    selected_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, option_xpath))
    )
    selected_option.click()

    print(f"Clicked on: {selected_time}")

    # Optionally, if there's a separate "Download" button, click it afterward
    # download_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download')]"))  # Adjust as needed
    # )
    # download_button.click()
    # print("Download initiated.")

    # Wait for the file to download (adjust as needed)
    time.sleep(10)  # Adjust time to ensure the image download completes

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
