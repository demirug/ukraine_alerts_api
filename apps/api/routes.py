import os
from datetime import datetime, date
from operator import and_

from flask import request, make_response, render_template, send_file, current_app

from application import cache
from apps.api.controller import api_blpr as api
from apps.api.models import Region, RegionStatus
from apps.api.schemas import RegionSchema, RegionStatusSchema, RegionShortStatusSchema, HistoryRegionStatusSchema
from apps.api.services import get_statuses, render_alert_img, parse_date, parse_uint


@api.route('/regions')
@cache.cached(key_prefix="%s")
def regionList():
    """
    Return: json list of all registered regions
    Fields: id, name, is_city
    """

    return RegionSchema(many=True).dump(Region.query.all())


@api.route('/status')
@cache.cached(key_prefix="%s")
def regionStatusList():
    """
    Return: json list of all current region statuses
    Fields: region_id, is_alert, timestamp
    """

    regions = get_statuses()

    if request.args.get("short", default=False, type=bool):
        return RegionShortStatusSchema(many=True).dump(regions)
    return RegionStatusSchema(many=True).dump(regions)


@api.route('/status/<int:region_id>')
@cache.cached(key_prefix="%s")
def regionStatusDetail(region_id):
    """
    Return: json of region current status
    Fields: region_id, is_alert, timestamp
    """

    region_status: RegionStatus = RegionStatus.query.filter(RegionStatus.region_id == region_id).order_by(
        RegionStatus.timestamp.desc()).first()
    if region_status is None:
        return {"status": "NOT FOUND"}, 404
    if request.args.get("short", default=False, type=bool):
        return RegionShortStatusSchema().dump(region_status)
    return RegionStatusSchema().dump(region_status)


@api.route('/history')
@cache.cached(key_prefix=lambda: request.full_path)
def regionsHistory():
    """
     Return history of regions
     Available args: from (date), to (date), limit (int > 1)
     Date format: %Y%m%d%H%M%S
    """

    from_date = request.args.get('from', default=date.min, type=parse_date)
    to_date = request.args.get('to', default=datetime.utcnow(), type=parse_date)
    limit = request.args.get('limit', default=1000, type=parse_uint)

    return HistoryRegionStatusSchema().dump(
        RegionStatus.query.filter(
            and_(RegionStatus.timestamp >= from_date, RegionStatus.timestamp <= to_date))
        .order_by(RegionStatus.timestamp.desc()).limit(limit), many=True)


@api.route('/history/<int:region_id>')
@cache.cached(key_prefix=lambda: request.full_path)
def regionHistory(region_id):
    """
     Return history of region by region_id
     Available args: from (date), to (date), limit (int > 1)
     Date format: %Y%m%d%H%M%S
    """

    region: Region = Region.query.filter_by(id=region_id).first()
    if not region:
        return {"status": "NOT FOUND"}, 404

    from_date = request.args.get('from', default=date.min, type=parse_date)
    to_date = request.args.get('to', default=datetime.utcnow(), type=parse_date)
    limit = request.args.get('limit', default=1000, type=parse_uint)

    return HistoryRegionStatusSchema().dump(
        RegionStatus.query.filter(and_(RegionStatus.region_id == region_id,
                                       and_(RegionStatus.timestamp >= from_date, RegionStatus.timestamp <= to_date)))
        .order_by(RegionStatus.timestamp.desc()).limit(limit), many=True)


@api.route('/renderHtml')
@cache.cached(key_prefix="%s")
def renderHtml():
    """ Render html alert map"""
    headers = {'Content-Type': 'text/html'}

    return make_response(render_template('map.html', reg_data={el.region_id: el.is_alert for el in get_statuses()}),
                         200, headers)


@api.route('/renderImage')
def renderImage():
    """ Render alert map image"""

    if not current_app.config['RENDER_ALERT_MAP']:
        return {"status": "NOT SUPPORTED"}, 404

    if not os.path.isfile("alert-map.png"):
        render_alert_img()

    return send_file("alert-map.png", mimetype='image/png')
