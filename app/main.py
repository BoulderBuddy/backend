from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.api.error_http import add_custom_exception_handlers
from app.core.config import settings
from app.db.database import create_database_scheme

app = FastAPI(title="BoulderBuddy")

if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

create_database_scheme()

add_custom_exception_handlers(app)
app.include_router(api_router)
