from pydantic.main import BaseModel

from .message import Message


class Update(BaseModel):
    update_id: int
    message: Message
