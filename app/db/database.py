import os
from typing import Annotated
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
from pathlib import Path

# Obtención del string connection desde .env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")

# Creación de engine
engine = create_engine(DATABASE_URL, echo=True)

# Creación de sesión
def get_session():
    with Session(engine) as session:
        yield session


# Creación de base de datos y tablas
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)