import time

from selenium import webdriver

url = "https://yandex.ru/search/?text=%D0%BF%D0%B5%D1%80%D0%B2%D1%8B%D0%B9+%D1%81%D0%BA%D1%80%D0%B8%D0%BD&lr=20728&clid=2411726"

browser = webdriver.Firefox()
browser.get(url)
time.sleep(10)
browser.get_screenshot_as_file("screen1.png")

# browser.refresh()
# time.sleep(4)
browser.get('https://yandex.ru/search/?text=%D0%B2%D1%82%D0%BE%D1%80%D0%BE%D0%B9+%D1%81%D0%BA%D1%80%D0%B8%D0%BD&lr=20728&clid=2411726')
time.sleep(10)
browser.get_screenshot_as_file("screen2.png")
browser.close()
browser.quit()
