"""from selenium import webdriver
from selenium.webdriver.common.by import By #the locator tool which will help it find buttons and fields in the web page

driver = webdriver.Chrome()# launches chrome
driver.get("https://www.google.com")

search_box = driver.find_element(By.NAME, "q")#finds the search text box
search_box.send_keys("geeksforgeeks")#types what we want to search in the bar
search_box.submit()#submits the search like hitting enter 
"""

"""
from selenium import webdriver
from selenium.webdriver.common.by import By # By used for location HTML elements
from time import sleep #pauses for 1 second before clicking next page

driver = webdriver.Chrome() #opens chrome

driver.get("https://quotes.toscrape.com/js/") #opens the web site

while True: #an infinite loop, it will only break when there is no 'next' button
    quotes = driver.find_elements(By.CLASS_NAME, "quote")# 'find_elements() lists all elements with class name quote
    for q in quotes:
        print("\n", q.text)#q.text prints it

    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "li.next > a") #find the next button
        next_btn.click()
        sleep(1)
    except:
        print("no more pages")
        break
    

"""

#automated form fillup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome()

# -----------------------------
# 1️⃣ Fill form on W3Schools
# -----------------------------
driver.get("https://www.w3schools.com/html/html_forms.asp")

driver.find_element(By.ID, "fname").send_keys("Ayush")
driver.find_element(By.ID, "lname").send_keys("Automation")

sleep(2)   # Just to observe before switching pages

# -----------------------------
# 2️⃣ Login automation
# -----------------------------
driver.get("https://the-internet.herokuapp.com/login")

driver.find_element(By.ID, "username").send_keys("tomsmith")
driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
driver.find_element(By.CSS_SELECTOR, "button.radius").click()

sleep(3)   # Let the login result load
