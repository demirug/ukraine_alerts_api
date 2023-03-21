import os

from flask import abort, request, make_response, render_template, send_file, current_app
from flask_restx import Resource

from api.models import Region, RegionStatus
from api.schemas import RegionSchema, RegionStatusSchema, RegionShortStatusSchema
from api.services import get_statuses, render_alert_img
from application import api


@api.route('/regions')
class RegionList(Resource):

    def get(self):
        """
        Return: json list of all registered regions
        Fields: id, name, is_city
        """

        return RegionSchema(many=True).dump(Region.query.all())


@api.route('/status')
class RegionStatusList(Resource):
    def get(self):
        """
        Return: json list of all current region statuses
        Fields: region_id, is_alert, timestamp
        """

        regions = get_statuses()

        if 'short' in request.args:
            return RegionShortStatusSchema(many=True).dump(regions)
        return RegionStatusSchema(many=True).dump(regions)


@api.route('/status/<int:id>')
class RegionStatus(Resource):
    def get(self, id):
        """
        Return: json of region current status
        Fields: region_id, is_alert, timestamp
        """

        region_status: RegionStatus = RegionStatus.query.filter(RegionStatus.region_id==id).order_by(RegionStatus.timestamp.desc()).first()
        if region_status is None:
            abort(404)
        if 'short' in request.args:
            return RegionShortStatusSchema().dump(region_status)
        return RegionStatusSchema().dump(region_status)


@api.route('/render')
class RenderMap(Resource):
    def get(self):
        """ Render html alert map"""
        headers = {'Content-Type': 'text/html'}

        return make_response(render_template('map.html', reg_data={el.region_id: el.is_alert for el in get_statuses()}),
                             200, headers)


@api.route('/renderImage')
class RenderMapImage(Resource):
    @api.produces(['image/png'])
    def get(self):
        """ Render alert map image"""

        if not current_app.config['RENDER_ALERT_MAP']:
            return send_file('static/not-provided.png', mimetype='image/png')

        if not os.path.isfile("alert-map.png"):
            render_alert_img()

        return send_file("static/alert-map.png", mimetype='image/png')
