from datetime import datetime
from typing import List

from sqlalchemy.orm import relationship, Mapped

from application import db
import sqlalchemy as sq


class Region(db.Model):
    __tablename__ = "regions"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(60), nullable=False, unique=True)
    is_city = sq.Column(sq.Boolean, default=False)

    statuses: Mapped[List["RegionStatus"]] = sq.orm.relationship('RegionStatus', back_populates="region")


class RegionStatus(db.Model):
    __tablename__ = "regions_status"

    id = sq.Column(sq.Integer, primary_key=True)
    region_id = sq.Column(sq.Integer, sq.ForeignKey('regions.id'), nullable=False)
    is_alert = sq.Column(sq.Boolean, nullable=False)
    timestamp = sq.Column(sq.DateTime, default=datetime.utcnow)

    region: Mapped["Region"] = sq.orm.relationship('Region', back_populates="statuses")


class CallbackClient(db.Model):
    id = sq.Column(sq.Integer, primary_key=True)
    url = sq.Column(sq.String, nullable=False)
    signature = sq.Column(sq.String, nullable=False)
    email = sq.Column(sq.String, nullable=False)
    paypal_order = sq.Column(sq.String, unique=True, nullable=False)
    payed = sq.Column(sq.Boolean, default=False)
    timestamp = sq.Column(sq.DateTime, default=datetime.utcnow)

