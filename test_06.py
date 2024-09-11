# Test Case
#-------------------------------------------
# 1.	Open Web Browser (Chrome/firefox/IE/Edge)
# 2.	Open URL https//admin-demo.nopcommercve.com/login
# 3.	Provide Email {admin@yourstore.com)
# 4.	Provide password {admin)
# 5.	Click Login
# 6.	Capture title of the dashboard page. (Actual title)
# 7.	Verify title of the page: “Dashboard /nopCommerce administration” (Expected)
# 8.	Close browser

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service_obj = Service("/home/chawas/Development/python/selenium/drivers/geckodriver-v0.35.0-linux64/geckodriver")
driver = webdriver.Firefox(service=service_obj)

#driver=webdriver.Chrome("E:\Development\Projects\Python\drivers\chrome\chromedriver.exe")

driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
#driver.get("https://www.rcvacademy.com")
driver.maximize_window()
print(driver.title)
driver.close()
#driver.find_element(By.NAME,"username").sendkeys("Admin")
#driver.find_element(By.ID,"password").sendkeys("admin123")