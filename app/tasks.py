from app.models import Region, RegionStatus
from app.services import get_or_create
from application import celery, db
from scrapping import get_alert_data


@celery.task
def update_status():
    for data in get_alert_data():
        region: Region = get_or_create(Region, name=data['name'], create={"is_city": data['is_city']})

        last_status: RegionStatus = RegionStatus.query.filter_by(region_id=region.id).order_by(RegionStatus.timestamp.desc()).first()

        if not last_status or last_status.is_alert != data['alert']:
            status: RegionStatus = RegionStatus(region_id=region.id, is_alert=data['alert'])

            db.session.add(status)
            db.session.commit()
