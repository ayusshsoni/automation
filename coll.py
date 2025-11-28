from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.add_argument("--headless")
options.set_preference("permissions.default.image", 2)

driver = webdriver.Firefox(options=options)
driver.set_window_size(1400, 900)

query = "mobile"
data = {"title": [], "price": [], "link": []}

for page in range(1, 20):
    url = f"https://www.amazon.in/s?k={query}&page={page}"
    driver.get(url)

    # LET THE PAGE LOAD PROPERLY
    time.sleep(2)

    # SELECT PRODUCT BLOCKS
    products = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item[data-asin]")
    print(f"Page {page} → {len(products)} products found")

    for p in products:
        try:
            title_elem = p.find_element(By.CSS_SELECTOR, "h2 a span")
            title = title_elem.text.strip()

            link = p.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")

            try:
                price = p.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.strip()
            except:
                price = None

            data["title"].append(title)
            data["price"].append(price)
            data["link"].append(link)

        except Exception as e:
            continue

driver.quit()

df = pd.DataFrame(data)
df.to_csv("amazon_products.csv", index=False)

print(f"Saved: {len(df)} rows")
