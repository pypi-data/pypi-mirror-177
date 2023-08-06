from pydantic import BaseModel, Field
from typing import List, Optional


class User(BaseModel):
    id: int


class Message(BaseModel):
    message_id: int
    from_field: Optional[User] = Field(..., alias="from")
    text: Optional[str]


class Update(BaseModel):
    update_id: int
    message: Optional[Message]


class ResponseUpdate(BaseModel):
    ok: bool
    result: List[Update]


class ResponseMassage(BaseModel):
    ok: bool
    result: Message
