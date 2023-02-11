from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Region, RegionStatus


class RegionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Region
        fields = ("id", "name", "is_city")


class RegionStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RegionStatus
        fields = ("id", "region_id", "is_alert", "timestamp")

