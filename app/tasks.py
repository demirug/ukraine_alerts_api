from app.models import Region, RegionStatus
from app.services import get_or_create
from application import celery, db
from scrapping import get_alert_data_selenium, get_alert_data_api


@celery.task
def update_status_api():
    __update_data(get_alert_data_api())


@celery.task
def update_status_selenium():
    __update_data(get_alert_data_selenium())


def __update_data(data: []):
    """
    Update database with data
    :param data: list of dicts with structure {name: value, is_alert: value, is_city: value}
    """
    for el in data:
        region: Region = get_or_create(Region, name=el['name'], create={"is_city": el['is_city']})

        last_status: RegionStatus = RegionStatus.query.filter_by(region_id=region.id).order_by(
            RegionStatus.timestamp.desc()).first()

        if not last_status or last_status.is_alert != el['alert']:
            status: RegionStatus = RegionStatus(region_id=region.id, is_alert=el['alert'])

            db.session.add(status)
            db.session.commit()
