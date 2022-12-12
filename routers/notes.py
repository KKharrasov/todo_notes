from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.utils import get_db
from user import errors, service
from user.responses import with_errors
from app.models import *
from app.schemas import *


note_router = APIRouter()


@note_router.get('/api/v1/todos', response_model=List[NoteList])
def list_of_todos(
        db: Session = Depends(get_db),
        user: User = Depends(service.get_current_user)
):
    return db.query(Note).filter(Note.user_id == user.id).all()


@note_router.post('/api/v1/todos')
def new_todo(
        item: NoteCreate,
        db: Session = Depends(get_db),
        user: User = Depends(service.get_current_user),
):
    note = Note(**item.dict())
    note.user_id = user.id
    note.created_timestamp = datetime.now()
    note.status = Status.not_started
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@note_router.put('/api/v1/todos/:{id}',
                 response_model=NoteUpdate,
                 responses=with_errors(
                errors.bad_token,
                errors.user_not_found,
                errors.post_not_found()),
                 )
def update_todo(
        id: int,
        status: Status,
        # params: NoteCreate,
        user: User = Depends(service.get_current_user),
        db: Session = Depends(get_db),
):
    note = db.query(Note).filter(Note.id == id).first()
    try:
        if note.user_id != user.id:
            raise errors.post_not_found()
    except AttributeError:
        raise errors.post_not_found()
    # note.name = params.name
    # note.description = params.description
    note.updated_timestamp = datetime.now()
    note.status = status
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@note_router.delete('/api/v1/todos/:{id}',
                    responses=with_errors(
                errors.bad_token,
                errors.user_not_found,
                errors.post_not_found()),
                    )
def delete_todo(
        id: int,
        user: User = Depends(service.get_current_user),
        db: Session = Depends(get_db),
):
    note = db.query(Note).filter(Note.id == id).first()
    try:
        if note.user_id != user.id:
            raise errors.post_not_found()
    except AttributeError:
        raise errors.post_not_found()
    db.delete(note)
    db.flush()
    return note
