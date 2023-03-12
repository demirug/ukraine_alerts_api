from flask import abort, request, make_response, render_template
from flask_restx import Resource

from api.models import Region, RegionStatus
from api.schemas import RegionSchema, RegionStatusSchema, RegionShortStatusSchema
from api.services import get_statuses
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

