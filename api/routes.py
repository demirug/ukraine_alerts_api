from flask import abort, request
from flask_restx import Resource
from sqlalchemy import func, and_

from api.models import Region, RegionStatus
from api.schemas import RegionSchema, RegionStatusSchema, RegionShortStatusSchema
from application import db, api


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

        Using SQL Query to get regions statuses

        SELECT r.* FROM
            (SELECT region_id, MAX(TIMESTAMP) AS timestamp FROM regions_status GROUP BY region_id) c
        JOIN regions_status r ON r.region_id = c.region_id and r.timestamp = c.timestamp
        """

        stmt = db.session.query(RegionStatus.region_id.label('region_id'),
                                func.MAX(RegionStatus.timestamp).label('timestamp')).group_by(
            RegionStatus.region_id).subquery()

        regions = RegionStatus.query.join(stmt, and_(RegionStatus.region_id == stmt.c.region_id,
                                                     RegionStatus.timestamp == stmt.c.timestamp)).all()

        if 'short' in request.args:
            return RegionShortStatusSchema(many=True).dump(regions)
        return RegionStatusSchema(many=True).dump(regions)


@api.route('/status/<int:id>')
class RegionStatusList(Resource):
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

