from fastapi import APIRouter

from .endpoints import exercise, parameter, session, users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(exercise.router, prefix="/exercises", tags=["excercises"])
api_router.include_router(parameter.router, prefix="/parameters", tags=["parameters"])
api_router.include_router(session.router, prefix="/sessions", tags=["sessions"])
