from fastapi import FastAPI

from app.api import api_router
from app.api.error_http import add_custom_exception_handlers
from app.db.database import create_database_scheme

app = FastAPI(title="BoulderBuddy")

create_database_scheme()

add_custom_exception_handlers(app)
app.include_router(api_router)
