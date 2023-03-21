import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_alerts_alerts_com_ua_API(url="https://alerts.com.ua/api/states"):
    res = requests.get(url, headers={"X-API-Key": os.getenv("ALERTS-COM-UA-API-KEY")})
    if res.status_code != 200:
        return []

    data = res.json()
    return [{"name": el['name'].replace(" область", ""), "alert": el['alert'], 'is_city': el['name'].startswith('м.')}
            for el in data['states']]


def get_alerts_ukrainealarm_com_API(url="https://api.ukrainealarm.com/api/v3/alerts", reg_url="https://api.ukrainealarm.com/api/v3/regions"):
    if not hasattr(get_alerts_ukrainealarm_com_API, "regions") or not get_alerts_ukrainealarm_com_API.regions:
        # Getting regions list
        res_reg = requests.get(reg_url, headers={"Authorization": os.getenv("UKRAINE-ALARM-COM-API-KEY")})
        if res_reg.status_code == 200:
            # Get regions list without Test region
            get_alerts_ukrainealarm_com_API.regions = [el["regionName"].replace(" область", "") for el in
                                               res_reg.json()["states"] if el["regionId"] not in ["0"]]

    res = requests.get(url, headers={"Authorization": os.getenv("UKRAINE-ALARM-COM-API-KEY")})
    if res.status_code != 200:
        return []

    alert_reg = [el['regionName'].replace(" область", "") for el in res.json() if
                 el['regionName'].replace(" область", "") in get_alerts_ukrainealarm_com_API.regions]

    out_data = [{"name": el, "alert": False, "is_city": el.startswith("м.")} for el in get_alerts_ukrainealarm_com_API.regions
                if el not in alert_reg]

    return out_data + [{"name": el, "alert": True, "is_city": el.startswith("м.")} for el in alert_reg]


def get_alerts_vadimklimenko_statuses(url="https://vadimklimenko.com/map/statuses.json"):
    replace = {
        "АР Крим": "Автономна Республіка Крим",
        "Севастополь'": "м. Севастополь"
    }

    data = requests.get(url).json()
    rg_info = []
    for name, dat in data['states'].items():
        if name in replace:
            name = replace[name]

        rg_info.append(
            {"name": name.replace(" область", ""), "alert": dat['enabled'], "is_city": name.startswith('м.')})
    return rg_info


def get_alerts_alerts_in_ua_selenium(url="https://alerts.in.ua"):
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
