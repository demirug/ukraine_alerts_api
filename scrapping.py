import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_alert_data(url="https://alerts.in.ua"):


def get_alert_data_selenium(url="https://alerts.in.ua"):
    options = webdriver.ChromeOptions()

    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)  # Time to load JS script 100%
    content = driver.find_elements(By.CSS_SELECTOR, "#map > svg > g.text-labels > text.map-label")
    data = list()

    for el in content:
        rs = {
            "name": el.get_attribute('aria-label'),
            "alert": 'active' in el.get_attribute('class').split(' '),
            "is_city": el.get_attribute('aria-label').startswith('м.')
        }
        if rs not in data:
            data.append(rs)

    driver.close()

    return data
