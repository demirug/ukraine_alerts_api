import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_alert_data(url="https://alerts.in.ua"):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)  # Time to load JS script 100%
    content = driver.find_elements(By.CSS_SELECTOR, "#map > svg > g.text-labels > text.map-label")
    driver.close()
    data = list()

    for el in set(content):
        data.append({
            "name": el.get_attribute('aria-label'),
            "alert": 'active' in el.get_attribute('class').split(' '),
            "is_city": el.get_attribute('aria-label').startswith('м.')
        })

    return data
