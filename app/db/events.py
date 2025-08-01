import copy

from fastapi.encoders import jsonable_encoder
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.models.waterGoal import WaterGoal
from app.models.waterGoalLog import WaterGoalLog
from app.utils.serializers import serialize_model, serialize_model_from_dict


def log_water_goal_change(session, action, instance, old_data=None, new_data=None):
    if not session:
        return
    log = WaterGoalLog(
        action=action,
        water_goal_id=instance.water_goal_id,
        user_id=instance.user_id,
        old_data=jsonable_encoder(old_data) if old_data else None,
        new_data=jsonable_encoder(new_data) if new_data else None,
    )
    session.add(log)


@event.listens_for(Session, "before_flush")
def receive_before_flush(session, flush_context, instances=None):
    # Guardar estado antigo para objetos alterados
    for obj in session.dirty:
        if isinstance(obj, WaterGoal) and session.is_modified(
            obj, include_collections=False
        ):
            # Copia profunda do estado antigo antes de flush
            # Podemos pegar dados do banco para 
            # garantir que seja o estado antes da modificação
            # Ou pegar do __dict__ (menos seguro se houver alteração prévia)
            old_state = {}
            for column in obj.__table__.columns:
                old_state[column.name] = getattr(obj, column.name)
            # Armazenar no objeto para depois usar no after_flush
            obj._old_state = copy.deepcopy(old_state)


@event.listens_for(Session, "after_flush")
def receive_after_flush(session, flush_context):
    # Criar logs após flush com id já definido
    for obj in session.new:
        if isinstance(obj, WaterGoal):
            log_water_goal_change(
                session=session,
                action="create",
                instance=obj,
                old_data=None,
                new_data=serialize_model(obj),
            )

    for obj in session.dirty:
        if isinstance(obj, WaterGoal) and session.is_modified(
            obj, include_collections=False
        ):
            old_data = getattr(obj, "_old_state", {})
            log_water_goal_change(
                session=session,
                action="update",
                instance=obj,
                old_data=serialize_model_from_dict(getattr(obj, "_old_state", {})),
                new_data=serialize_model(obj),
            )
            # Remover para liberar memória
            if hasattr(obj, "_old_state"):
                del obj._old_state

    for obj in session.deleted:
        if isinstance(obj, WaterGoal):
            log_water_goal_change(
                session=session,
                action="delete",
                instance=obj,
                old_data=serialize_model(obj),
                new_data=None,
            )
