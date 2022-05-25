import http
import logging
import time

from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.api.error_http import add_custom_exception_handlers
from app.core.config import settings
from app.db.database import create_database_scheme

logger = logging.getLogger("uvicorn")

app = FastAPI(title="BoulderBuddy")

if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time

    time_ms = process_time * 1000

    status = response.status_code
    status_text = http.HTTPStatus(status).phrase
    url = request.url.path
    host = request.client.host
    port = request.client.port
    method = request.method
    protocol_version = request.scope.get("http_version")

    mesg = '%s:%d - "%s %s HTTP/%s" %d %s - %.3f ms'
    logger.log(
        logging.INFO,
        mesg,
        host,
        port,
        method,
        url,
        protocol_version,
        status,
        status_text,
        time_ms,
    )

    response.headers["Server-Timing"] = ",".join([f"handle-request;dur={time_ms:.3f}"])

    return response


create_database_scheme()

add_custom_exception_handlers(app)
app.include_router(api_router)
