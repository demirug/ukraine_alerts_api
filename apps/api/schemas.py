from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apps.api.models import Region, RegionStatus


class RegionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Region
        fields = ("id", "name", "is_city")


class RegionStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RegionStatus
        fields = ("id", "region_id", "is_alert", "timestamp")


class RegionShortStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RegionStatus
        fields = ("region_id", "is_alert")
