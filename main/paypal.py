import json
import os

import requests
from requests.auth import HTTPBasicAuth

token = None


class GetTokenError(Exception):
    pass


def get_token():
    res = requests.post("https://api-m.sandbox.paypal.com/v1/oauth2/token", data={"grant_type": "client_credentials"},
                        auth=HTTPBasicAuth(os.getenv("PAYPAL-CLIENT"), os.getenv("PAYPAL-PASSWORD"))
                        )

    if res.status_code == 200:
        return json.loads(res.content)['token_type'] + " " + json.loads(res.content)['access_token']
    raise GetTokenError("Can't get token. Check your credentials and ethernet connection")


def api_request(path, data={}):
    global token
    if token is None:
        token = get_token()

    result = requests.post("https://api-m.sandbox.paypal.com" + path, json=data, headers={"Authorization": token})

    # On token expired
    if result.status_code == 401:
        token = None
        return api_request(path, data)

    return result.status_code, json.loads(result.content)


def create_order(value: float, currency="USD"):
    return api_request("/v2/checkout/orders", data={"intent": "CAPTURE", "purchase_units": [{"amount": {"currency_code": currency, "value": value}}]})[1]["id"]


def capture_payment(order_id):
    code, data = api_request(f"/v2/checkout/orders/{order_id}/capture")
    return code == 201 and data["status"] == "COMPLETED"
