## Ukraine alerts API

Scrapping information from alert info services and represent data in friendly format 

Production: https://air-raid-alert.pp.ua/

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)
---


## Installation
Client is based on `python 3.7`

To install dependencies use `pipenv` tool and run `pipenv install`

And run `flask db stamp head` to set migration version to highest

If you want to load regions with static `id` run `flask api load-defaults` (Use on empty database)

On updating project don't forget to run `flask db upgrade`

If you want to fetch data from https://alerts.in.ua/ by selenium: chrome webdriver needs to be installed

If you want to fetch data from https://alerts.com.ua/ API: Set api key for `ALERTS-COM-UA-API-KEY` variable in .env

If you want to fetch data from https://api.ukrainealarm.com/swagger/index.html API: set `UKRAINE-ALARM-COM-API-KEY` variable in .env

Alternative fetching data don't required additional settings (Might not be as fast/stability).

You can enable/disable fetch methods in `Config > CELERY_CONFIG > beat_schedule` by removing/adding them

### Setup  .env file

```
DEBUG=True
SECRET_KEY=MY_SUPER_SECRET_KEY

REDIS_URL=redis://127.0.0.1:6379/0

ALERTS-COM-UA-API-KEY=your_api_key
UKRAINE-ALARM-COM-API-KEY=your_api_key

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

At `/api` path displaying swagger page with all available api endpoints