import time

import chromedriver_binary
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get("https://scratch.mit.edu/explore/projects/all")

result = list()

for i in range(197):
    try:
        Select(driver.find_element(By.XPATH, '//*[@id="frc-language-1088"]')).select_by_index(i)
        driver.refresh()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except NoSuchElementException:
        break
    time.sleep(0.1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    cookie = driver.get_cookie("scratchlanguage")
    result.append(cookie["value"])

print(result)
try:
    if input("ファイルへ出力しますか[y/n] >>") == "y":
        with open("result.txt", "a") as f:
          f.write(str(result))
except EOFError:
    pass
