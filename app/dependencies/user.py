from uuid import UUID

from fastapi import HTTPException, Request

from app.utils.jwt import verify_token


def get_keycloak_id(request: Request) -> UUID:
    # auth_header = request.headers.get("Authorization")
    # if not auth_header or not auth_header.startswith("Bearer "):
    #     raise HTTPException(status_code=401, detail="Token de autenticação ausente")

    # token = auth_header.split(" ")[1]
    # return verify_token(token)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autenticação ausente")

    token = auth_header.split(" ")[1]

    keycloak_id = verify_token(token)

    return keycloak_id
