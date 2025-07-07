############
# MAIN API #
############

# Imports
from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.models import characters, powers
from app.routers import characters

# API configuration
app = FastAPI()

# Models initialization
@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

# Router connection
app.include_router(characters.router)


@app.get("/")
async def hola():
    return {"Message": "Welcome to Heroes and Villains API!"}