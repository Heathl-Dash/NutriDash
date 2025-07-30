from datetime import datetime
from sqlalchemy.orm import DeclarativeMeta

def serialize_model(model):
    if not isinstance(model.__class__, DeclarativeMeta):
        raise ValueError("O objeto fornecido não é um modelo SQLAlchemy.")

    data = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        if isinstance(value, datetime):
            data[column.name] = value.isoformat()
        else:
            data[column.name] = value
    return data

def serialize_model_from_dict(data: dict) -> dict:
    from datetime import datetime
    return {
        k: (v.isoformat() if isinstance(v, datetime) else v)
        for k, v in data.items()
    }
