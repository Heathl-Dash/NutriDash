def serialize_model(instance):
    return {
        column.name: getattr(instance, column.name)
        for column in instance.__table__.columns
    }