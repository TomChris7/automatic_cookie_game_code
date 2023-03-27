from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_driver_path = "C:\chromedriver_win32\chromedriver.exe"
s = Service(executable_path=chrome_driver_path)
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=s, options=option)
driver.get(url="http://orteil.dashnet.org/experiments/cookie/")

#item store
store = driver.find_elements(By.CSS_SELECTOR, value="#store b")
store_prices = [item.text.split("-")[-1].strip().replace(",", "") for item in store if item != '']
store_items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
store_ids = [item.get_attribute("id") for item in store_items]
store_dict = {}
for n in range(len(store_prices)):
    store_dict[store_prices[n]] = store_ids[n]
buyable_item = 0

###Time ranges###
#Current time
tCurrent = time.time()
#5 seconds timeout
timeout = tCurrent + 5
#5mins timeout
five_min = tCurrent + 300

#getting cookie to click on
cookie = driver.find_element(by=By.ID, value="cookie")


while True:
    cookie.click()
    money = driver.find_element(By.CSS_SELECTOR, value="#money").text.replace(",", "")
    # Check store after 5secs
    if time.time() > timeout:
        for price in store_prices:
            if price != "" and int(money) >= int(price):
                buyable_item = price
        store_item = driver.find_element(By.ID, value=f"{store_dict[buyable_item]}")
        store_item.click()
        #add an extra 5 secs
        timeout = time.time() + 5

    #After 5mins has elaspsed
    if time.time() > five_min:
        cookie_per_sec = driver.find_element(By.ID, value="cps")
        print(cookie_per_sec.text)
        break

time.sleep(10)
