from datetime import datetime

from flask import render_template
from html2image import Html2Image
from sqlalchemy import func, and_

from apps.api.models import Region, RegionStatus
from application import db, cache

hti = Html2Image()


def get_statuses():
    stmt = db.session.query(RegionStatus.region_id.label('region_id'),
                            func.MAX(RegionStatus.timestamp).label('timestamp')).group_by(
        RegionStatus.region_id).subquery()

    return RegionStatus.query.join(stmt, and_(RegionStatus.region_id == stmt.c.region_id,
                                              RegionStatus.timestamp == stmt.c.timestamp)).all()


def __delete_cache_path_with_args(path):
    """ Works only with RedisCache """
    cache.delete(path)
    for key in cache.cache._write_client.keys(f"flask_cache_{path}*"):
        cache.delete(key.decode("UTF-8")[12:])


def delete_cache(new_statuses, new_regions: bool):
    """
    On receiving new regions information, delete old cache
    :param new_statuses: Single or list of regions id which received new alert statuses
    :param new_regions: Is a new region(s) registered
    """
    if not isinstance(new_statuses, list):
        new_statuses = [new_statuses]

    cache.delete("/api/status")
    for el in new_statuses:
        cache.delete(f"/api/status/{el}")
    cache.delete("/api/renderHtml")
    __delete_cache_path_with_args("/api/history")

    for el in new_statuses:
        __delete_cache_path_with_args(f"/api/history/{el}")

    if new_regions:
        cache.delete("/api/regions")


def parse_date(data):
    """ Parsing date for arguments """
    res = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%f")
    return res


def parse_uint(data):
    """ Parsing positive int for arguments """
    val = abs(int(data))
    if val == 0:
        raise ValueError("Value must be greater than 0")
    return val


def render_alert_img():
    hti.screenshot(
        html_str=render_template('map.html', reg_data={el.region_id: el.is_alert for el in get_statuses()}),
        css_str="html { background-color: black; }",
        save_as='alert-map.png',
        size=(600, 400)
    )


def get_or_create(model, create={}, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs, **create)

        db.session.add(instance)
        db.session.commit()

        return instance, True


def init_regions():
    if Region.query.count() == 0:
        db.session.add_all([
            Region(id=1, name="Закарпатська", is_city=False),
            Region(id=2, name="Хмельницька", is_city=False),
            Region(id=3, name="Одеська", is_city=False),
            Region(id=4, name="Дніпропетровська", is_city=False),
            Region(id=5, name="Черкаська", is_city=False),
            Region(id=6, name="м. Севастополь", is_city=True),
            Region(id=7, name="Запорізька", is_city=False),
            Region(id=8, name="Івано-Франківська", is_city=False),
            Region(id=9, name="Полтавська", is_city=False),
            Region(id=10, name="Луганська", is_city=False),
            Region(id=11, name="м. Київ", is_city=False),
            Region(id=12, name="Автономна Республіка Крим", is_city=False),
            Region(id=13, name="Донецька", is_city=False),
            Region(id=14, name="Чернівецька", is_city=False),
            Region(id=15, name="Миколаївська", is_city=False),
            Region(id=16, name="Рівненська", is_city=False),
            Region(id=17, name="Чернігівська", is_city=False),
            Region(id=18, name="Львівська", is_city=False),
            Region(id=19, name="Кіровоградська", is_city=False),
            Region(id=20, name="Харківська", is_city=False),
            Region(id=21, name="Херсонська", is_city=False),
            Region(id=22, name="Житомирська", is_city=False),
            Region(id=23, name="Тернопільська", is_city=False),
            Region(id=24, name="Київська", is_city=False),
            Region(id=25, name="Сумська", is_city=False),
            Region(id=26, name="Вінницька", is_city=False),
            Region(id=27, name="Волинська", is_city=False),
        ])
        db.session.commit()
        cache.delete("/api/regions")
