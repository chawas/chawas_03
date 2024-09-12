from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service_obj = Service("/home/chawas/.wdm/drivers/chromedriver/linux64/128.0.6613.119/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service_obj)

#driver=webdriver.Chrome("E:\Development\Projects\Python\drivers\chrome\chromedriver.exe")

#driver.get("https://demo.nopcommerce.com")
driver.get("https://www.facebook.com/")
driver.maximize_window()

driver.find_element(By.CSS_SELECTOR,"input.inputtext[data-testid=royal_pass]").send_keys("xyz")

#print(driver.title)
#driver.close()
