from fastapi import APIRouter, Depends
from app.tasks.publisher import publish_delete_user
from app.dependencies.user import get_user_id

router = APIRouter()

@router.post("/delete-user/")
def delete_user_endpoint(user_id:int = Depends(get_user_id)):
    publish_delete_user(user_id)
    return {"message": f"Pedido de exclusão para user_id {user_id} enviado."}
