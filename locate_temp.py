from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("https://www.flipkart.com/")

# search
search = driver.find_element(By.ID, "twotabsearchtextbox")
search.send_keys("mobile")
search.submit()

# WAIT for .puisg-row to appear
elem = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".puisg-row"))
)

print("FOUND:", elem.text)
