# app/utils/jwt.py
import jwt
from fastapi import HTTPException, status
from jwt import PyJWTError

SECRET_KEY = "Havoc"
ALGORITHM = "HS256"  # ou RS256, dependendo do emissor

def verify_token(token: str):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = payload.get("user_id") 
    if user_id is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido: ID ausente"
      )
    return user_id
  except PyJWTError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token inválido"
    )
