import os
import uuid

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from jwt import PyJWKClient

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
AUDIENCE = os.getenv("AUDIENCE")
URL_CERTS = os.getenv("URL_CERTS")

jwks_client = PyJWKClient(URL_CERTS)


def verify_token(token: str) -> uuid.UUID:
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        print(signing_key.key)

        payload = jwt.decode(
            token, signing_key.key, algorithms=[ALGORITHM], audience=AUDIENCE
        )
        print(payload)

        raw_id = payload.get("sub")
        print(raw_id)

        if not raw_id:
            raise HTTPException(status_code=401, detail="ID ausente no token")

        return uuid.UUID(raw_id)

    except jwt.exceptions.PyJWKClientError:
        raise HTTPException(
            status_code=503, detail="Não foi possível obter as chaves do Keycloak"
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except (jwt.InvalidTokenError, ValueError) as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")
