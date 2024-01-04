from src.config import postgres_settings
from .db import Database


db = Database(db_url=postgres_settings.db_uri)


def get_db():
    return db
