from pydantic import BaseModel
from datetime import datetime
from enum import Enum


BaseModel.Config.orm_mode = True


class Status(str, Enum):
    not_started = 'NotStarted'
    on_going = 'OnGoing'
    completed = 'Completed'


class NoteBase(BaseModel):
    name: str
    description: str
    created_timestamp: datetime
    updated_timestamp: datetime = None


class NoteList(NoteBase):
    id: int
    user_id: int
    status: Status


class NoteCreate(BaseModel):
    name: str
    description: str


class NoteUpdate(NoteCreate):
    status: Status
