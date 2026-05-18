import os
from sqlalchemy import Engine, create_engine
import json

engine: Engine

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
    )
ECHO = json.loads(os.getenv('ALCHEMY_ECHO').lower())
print(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=ECHO)