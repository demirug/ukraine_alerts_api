## Ukraine alerts API

Scrapping information from alert info services and represent data in friendly format 

Production: https://air-raid-alert.pp.ua/

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)
---


## Installation
Client is based on `python 3.7`

To install dependencies use `pipenv` tool and run `pipenv install`

If you want to fetch data with selenium task: chrome webdriver needs to be installed

If you want to fetch data from https://alerts.com.ua/ API: Set api key for `ALERTS-COM-UA-API-KEY` variable in .env

Alternative fetching data don't required additional settings (Might not be as fast/stability)

You can enable/disable fetch methods in `Config > CELERY_CONFIG > beat_schedule` by removing/adding them

### Setup  .env file

```
DEBUG=True
SECRET_KEY=MY_SUPER_SECRET_KEY

REDIS_URL=redis://127.0.0.1:6379/0

ALERTS-COM-UA-API-KEY=your_api_key

PAYPAL-CLIENT=blablabla_client
PAYPAL-PASSWORD=blablabla_password
```

### Setup celery
Running Celery worker

    celery -A worker.celery worker -l info
On Windows based server use

    celery -A worker.celery worker -l info -P evetlet
Running celery beat

    celery -A worker.celery beat -l info

---

## REST API

At root page displaying swagger


### Get regions list


    curl -X 'GET' 'http://127.0.0.1:5000/api/regions' -H 'accept: application/json'

#### Response

    HTTP/1.1 200 OK
    Connection: close
    Content-Type: application/json

    [
      {
        "name": "Миколаївська",
        "id": 1,
        "is_city": false
      },
      {
        "name": "Полтавська",
        "id": 2,
        "is_city": false
      }
    ]

---

### Get all region statuses


    curl -X 'GET' 'http://127.0.0.1:5000/api/status' -H 'accept: application/json'

#### Response

    HTTP/1.1 200 OK
    Connection: close
    Content-Type: application/json

    [
      {
        "timestamp": "2023-02-11T10:23:13.292580",
        "region_id": 1,
        "id": 1,
        "is_alert": false
      },
      {
        "timestamp": "2023-02-11T10:23:13.308209",
        "region_id": 2,
        "id": 2,
        "is_alert": false
      }
    ]

---

### Get region status by region id


    curl -X 'GET' 'http://127.0.0.1:5000/api/status/1' -H 'accept: application/json'

#### Response

    HTTP/1.1 200 OK
    Connection: close
    Content-Type: application/json

    {
      "region_id": 1,
      "is_alert": false,
      "id": 1,
      "timestamp": "2023-02-11T10:23:13.292580"
    }

---