from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.models import heroes, villains, powers
from app.routers import heroes, villains

app = FastAPI()

# Inicialización de modelos
@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

# Conexión con routers
app.include_router(heroes.router)
app.include_router(villains.router)



@app.get("/")
async def hola():
    return {"message": "hola app!"}