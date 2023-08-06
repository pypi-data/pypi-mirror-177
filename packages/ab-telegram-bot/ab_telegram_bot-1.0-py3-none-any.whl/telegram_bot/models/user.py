from pydantic.main import BaseModel


class User(BaseModel):
    id: int
