from fastapi import Header, HTTPException

def get_user_id(x_user_id: int = Header(...)):
  if not x_user_id:
    return HTTPException(status_code=400, detail="X-User-Id não enviado")