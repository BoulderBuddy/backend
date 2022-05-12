import logging
from functools import lru_cache
from typing import Union

from pydantic import AnyHttpUrl, BaseSettings, validator

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = False
    backend_cors_origins: list[AnyHttpUrl] = []

    @validator("backend_cors_origins", pre=True)
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


@lru_cache()
def get_settings() -> Settings:
    x = Settings()
    log.info("Loaded config settings: %s", x)
    return x


settings = get_settings()
