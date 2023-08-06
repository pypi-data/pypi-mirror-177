from pydantic.fields import Field
from pydantic.main import BaseModel

from .user import User


class Message(BaseModel):
    message_id: int
    text: str
    from_user: User = Field(alias='from')
