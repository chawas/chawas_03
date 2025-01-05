from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Specify the path to the desired Chromedriver
chromedriver_path = "/usr/local/bin/chromedriver"  # Update this path if needed

service = Service(chromedriver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.google.com")
print("Page title:", driver.title)
driver.quit()
