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

