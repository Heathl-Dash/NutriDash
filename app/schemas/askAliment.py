from pydantic import BaseModel


class AskAliment(BaseModel):
    aliment: str
