from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os

os.makedirs("data", exist_ok=True)

driver = webdriver.Firefox()
query = "mobile"
file = 0

for i in range(1, 20):
    url = f"https://www.amazon.in/s?k={query}&page={i}"
    driver.get(url)
    time.sleep(3)

    # MAIN PRODUCT BLOCKS
    items = driver.find_elements(By.XPATH, "//div[@data-asin!='' and contains(@class,'s-result-item')]")
    print(f"Page {i} → {len(items)} products found")

    for item in items:
        html = item.get_attribute("outerHTML")
        with open(f"data/{query}_{file}.html", "w", encoding="utf-8") as f:
            f.write(html)
        file += 1

driver.quit()
