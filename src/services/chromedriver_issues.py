from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Explicitly specify the ChromeDriver path
service = Service("/usr/bin/chromedriver")  # Adjust this path if necessary
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode if no GUI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Test the setup
driver.get("https://www.google.com")
print("Page title:", driver.title)

driver.quit()
