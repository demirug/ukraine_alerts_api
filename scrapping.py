import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_alert_data_api(url="https://alerts.com.ua/api/states"):
    res = requests.get(url, headers={"X-API-Key": os.getenv("ALERTS-COM-UA-API-KEY")})
    if res.status_code != 200:
        return []

    data = res.json()
    return [{"name": el['name'].replace(" область", ""), "alert": el['alert'], 'is_city': el['name'].startswith('м.')} for el in data['states']]


def get_alert_data_mirror(url="https://vadimklimenko.com/map/statuses.json"):

    replace = {
        "АР Крим": "Автономна Республіка Крим",
        "Севастополь'": "м. Севастополь"
    }

    data = requests.get(url).json()
    rg_info = []
    for name, dat in data['states'].items():
        if name in replace:
            name = replace[name]

        rg_info.append({"name": name.replace(" область", ""), "alert": dat['enabled'], "is_city": name.startswith('м.')})
    return rg_info


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
    content = driver.find_elements(By.CSS_SELECTOR, "path.map-district")
    data = list()

    for el in content:
        rs = {
            "name": el.get_attribute('data-oblast').replace(" область", ""),
            "alert": el.get_attribute('data-alert-type') != "",
            "is_city": el.get_attribute('data-oblast').startswith('м.')
        }
        if rs not in data:
            data.append(rs)

    driver.close()

    return data
