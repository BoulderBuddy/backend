from fastapi import FastAPI

from app.api import api_router
from app.api.error_http import add_custom_exception_handlers

app = FastAPI(title="BoulderBuddy")


add_custom_exception_handlers(app)
app.include_router(api_router)


# @app.get("/")
# def read_root(settings: Settings = Depends(get_settings)):
#     return {"Environment": settings.environment, "Testing": settings.testing}


# @app.get("/sessions/", response_model=list[schemas.TrainingSession])
# def read(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return crud.trainingsession.get_multi(db, skip=skip, limit=limit)
