import json
import secrets
import string

from flask import render_template, request, url_for, abort, redirect, current_app

from api.models import CallbackClient
from application import db
from main.controller import main as app
from main.forms import CallbackOrderForm
from main.paypal import create_order, capture_payment


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/callback", methods=["GET", "POST"])
def callback():
    form = CallbackOrderForm()

    if form.validate_on_submit():
        client = CallbackClient(
            signature=''.join(secrets.choice(string.ascii_lowercase + string.digits) for i in range(32)),
            url=form.url.data,
            email=form.email.data,
            paypal_order=create_order(current_app.config["CALLBACK_REGISTER_PRICE"])
        )

        db.session.add(client)
        db.session.commit()

        return redirect(url_for(".checkout", callback_id=client.id))
    return render_template("callback.html", form=form)


@app.route("/checkout/<int:callback_id>", methods=["GET", "POST"])
def checkout(callback_id):
    callback_client = CallbackClient.query.get(callback_id)
    if callback_client is None:
        abort(404)

    if callback_client.payed:
        return render_template("checkout_success.html", object=callback_client)

    if request.method == "POST":
        return json.dumps({"id": callback_client.paypal_order})
    else:
        return render_template("checkout.html", object=callback_client)


@app.route("/checkout/<int:callback_id>/capture", methods=["POST"])
def checkout_capture(callback_id):
    callback_client = CallbackClient.query.get(callback_id)
    if callback_client is None or callback_client.payed:
        abort(404)

    if capture_payment(callback_client.paypal_order):
        callback_client.payed = True
        db.session.add(callback_client)
        db.session.commit()

        return json.dumps({"status": "OK"})
    return json.dumps({"status": "Error"})
