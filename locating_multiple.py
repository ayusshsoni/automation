from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
query="mobile"
for i in range(1, 20):
    driver.get(f"https://www.amazon.in/s?k={query}&page={i}&xpid=Sj3xjntovZGEB&crid=10WXMDZPDFZ6I&qid=1764333670&sprefix=mobile%2Caps%2C262&ref=sr_pg_2")


    elems=driver.find_elements(By.CLASS_NAME, "puisg-row")
    print(f"{len(elems)} items found")
    for elem in elems:
        print(elem.text)

#print(elem.get_attribute("outerHTML"))
    print(elems)
#print(elem.get_text)

    time.sleep(3)
    driver.close()