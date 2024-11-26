from dataclasses import dataclass
from os import environ


@dataclass
class Settings:
    SECRET_KEY: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str


settings = Settings(
    SECRET_KEY=environ["SECRET_KEY"],
    POSTGRES_USER=environ["POSTGRES_USER"],
    POSTGRES_PASSWORD=environ["POSTGRES_PASSWORD"],
    POSTGRES_HOST=environ["POSTGRES_HOST"],
    POSTGRES_PORT=int(environ["POSTGRES_PORT"]),
    POSTGRES_DB=environ["POSTGRES_DB"],
)
