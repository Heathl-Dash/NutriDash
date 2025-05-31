# from fastapi import Header, HTTPException

# def get_user_id(x_user_id: int = Header(...)):
#     if not x_user_id:
#         raise HTTPException(status_code=400, detail="X-User-Id não enviado")
#     return x_user_id

from fastapi import Depends, Request
from app.utils.jwt import verify_token
from fastapi import Header, HTTPException

def get_user_id(request: Request) -> int:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autenticação ausente")

    token = auth_header.split(" ")[1]
    return verify_token(token)
