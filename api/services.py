from api.models import Region
from application import db


def get_or_create(model, create={}, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs, **create)

        db.session.add(instance)
        db.session.commit()

        return instance


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
