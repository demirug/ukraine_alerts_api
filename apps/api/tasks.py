from datetime import datetime

import requests
from flask import current_app

from apps.api.models import Region, RegionStatus, CallbackClient
from apps.api.schemas import RegionStatusSchema
from apps.api.services import get_or_create, render_alert_img
from application import celery, db, cache
from scrapping import get_alerts_alerts_in_ua_selenium, get_alerts_vadimklimenko_statuses, get_alerts_alerts_com_ua_API, \
    get_alerts_ukrainealarm_com_API


@celery.task
def update_status_ukrainealarm_com_API():
    __update_data(get_alerts_ukrainealarm_com_API())


@celery.task
def update_status_alerts_com_ua_API():
    __update_data(get_alerts_alerts_com_ua_API())


@celery.task
def update_status_alerts_in_ua_selenium():
    __update_data(get_alerts_alerts_in_ua_selenium())


@celery.task
def update_status_vadimklimenko_statuses():
    __update_data(get_alerts_vadimklimenko_statuses())


@celery.task
def inform_callback_clients(region_status_id):
    obj = RegionStatus.query.get(region_status_id)
    if obj is None:
        return

    json_data = RegionStatusSchema().dump(obj)
    for client in CallbackClient.query.filter_by(payed=True):
        try:
            requests.post(client.url, json=json_data, headers={"X-API-Key": client.signature}, timeout=1)
        except Exception:
            pass


def __update_data(data: []):
    """
    Update database with data
    :param data: list of dicts with structure {name: value, is_alert: value, is_city: value}
    """
    new_informs = []

    for el in data:
        region, created = get_or_create(Region, name=el['name'], create={"is_city": el['is_city']})

        if created:
            cache.delete("/api/regions")

        if region.static:
            continue

        last_status: RegionStatus = RegionStatus.query.filter_by(region_id=region.id).order_by(
            RegionStatus.timestamp.desc()).first()

        if not last_status or last_status.is_alert != el['alert']:
            status: RegionStatus = RegionStatus(region_id=region.id, is_alert=el['alert'], timestamp=datetime.utcnow)
            db.session.add(status)

            if last_status:
                last_status.end_timestamp = status.timestamp
                db.session.add(last_status)

            new_informs.append(status)

    if new_informs:
        db.session.commit()

        cache.delete_many([f"/api/status/{el.region_id}" for el in new_informs])
        cache.delete("/api/status")
        cache.delete("/api/renderHtml")

        if current_app.config['RENDER_ALERT_MAP']:
            render_alert_img()
            cache.delete("/api/renderImage")

        for status in new_informs:
            inform_callback_clients.delay(status.id)
