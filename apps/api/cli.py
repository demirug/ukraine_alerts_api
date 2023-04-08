import click
from flask import current_app

from apps.api.controller import api_blpr
from apps.api.models import Region, RegionStatus
from application import db, cache
from apps.api.services import init_regions, render_alert_img
from apps.api.tasks import inform_callback_clients


@api_blpr.cli.command("regions")
def region_list():
    print(f"Region count: {Region.query.count()}")
    for elm in Region.query.all():
        print(f"#{elm.id}. {elm.name}")


@api_blpr.cli.command("load-defaults")
def default_regions():
    init_regions()
    print("Default regions loaded")


@api_blpr.cli.command("region")
@click.argument('id')
@click.argument('action')
def region_action(id, action):
    """
     Action list:
     static - Change region static status to reverse
     alert - Change alert status to reverse
     info - Print information about region
    """

    region: Region = Region.query.filter_by(id=id).first()
    if region is None:
        print(f"Region with id {id} not found")
    else:
        if action == "static":
            region.static = not region.static
            db.session.add(region)
            db.session.commit()

            print(f"Region {region.name} static changed to {region.static}")
        elif action == "alert":
            last_status = RegionStatus.query.filter_by(region_id=region.id).order_by(
                RegionStatus.timestamp.desc()).first()

            if last_status is None:
                is_alert = True
            else:
                is_alert = not last_status.is_alert
            status = RegionStatus(region_id=region.id, is_alert=is_alert)
            db.session.add(status)
            db.session.commit()

            cache.delete(f"/api/status/{region.id}")
            cache.delete("/api/status")
            cache.delete("/api/renderHtml")

            print(f"Region {region.name} alert status changed to {status.is_alert}")

            if current_app.config['RENDER_ALERT_MAP']:
                render_alert_img()

            inform_callback_clients.delay(status.id)
        elif action == "info":
            last_status = RegionStatus.query.filter_by(region_id=region.id).order_by(
                RegionStatus.timestamp.desc()).first()

            if last_status is None:
                is_alert = False
            else:
                is_alert = last_status.is_alert

            print(f"Region {region.name}")
            print(f"Id: {region.id}")
            print(f"Static: {region.static}")
            print(f"Is alert: {is_alert}")
            if is_alert:
                print(f"Alert start datetime: {last_status.timestamp}")
        else:
            print("Unknown action")
