from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
query="mobile"
driver.get(f"https://www.amazon.in/s?k={query}&crid=195F4DA0UJYM1&sprefix=mobile%2Caps%2C266&ref=nb_sb_noss_2")
elem=driver.find_element(By.CLASS_NAME, "puisg-row")
print(elem.get_attribute("outerHTML"))
time.sleep(3)
driver.close()