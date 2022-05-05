from fastapi import FastAPI

from app.api import api_router
from app.api.error_http import add_custom_exception_handlers

app = FastAPI(title="BoulderBuddy")


add_custom_exception_handlers(app)
app.include_router(api_router)


# @app.get("/")
# def read_root(settings: Settings = Depends(get_settings)):
#     return {"Environment": settings.environment, "Testing": settings.testing}


# @app.get("/workouts/", response_model=list[schemas.Workout])
# def read_workouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return crud.workout.get_multi(db, skip=skip, limit=limit)
