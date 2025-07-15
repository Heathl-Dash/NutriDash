from fastapi import Request
from app.utils.jwt import verify_token
from fastapi import HTTPException

def get_user_id(request: Request) -> int:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autenticação ausente")

    token = auth_header.split(" ")[1]
    return verify_token(token)
