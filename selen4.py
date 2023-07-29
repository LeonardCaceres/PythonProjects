from selenium import webdriver
import time
from selenium.webdriver.common.by import By

login = input('YOUR_LOGIN')
password = input('YOUR_PASSWORD')

#options

options = webdriver.FirefoxOptions()

browser = webdriver.Firefox(options=options)

try:
    browser.get("https://account.mail.ru")
    time.sleep(5)
    print(0)
    email_input = browser.find_elements(By.TAG_NAME, "input")[0]
    email_input.clear()
    time.sleep(2)
    print(1)
    email_input.send_keys(login)
    print(2)
    button_email = browser.find_elements(By.TAG_NAME, "button")[1]
    button_email.click()
    time.sleep(10)
    page = browser.page_source
    with open('mail.html', 'w', encoding='utf-8') as file:
        file.write(page)
    password_input = browser.find_elements(By.TAG_NAME, "input")[2]
    time.sleep(2)
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(5)
    button_email = browser.find_elements(By.TAG_NAME, "button")[1]
    button_email.click()
    x = input()
except Exception as ex:
    print(ex)
finally:
    browser.close()
    browser.quit()