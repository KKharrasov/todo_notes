from fastapi import APIRouter
from routers import notes, auth


routes = APIRouter()
routes.include_router(notes.note_router)
routes.include_router(auth.auth_router)



