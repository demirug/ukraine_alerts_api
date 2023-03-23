from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms import validators


class CallbackOrderForm(FlaskForm):
    url = StringField("Url", validators=[validators.DataRequired()])
    email = EmailField("Email", validators=[validators.DataRequired()])

