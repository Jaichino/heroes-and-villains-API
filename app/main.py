############
# MAIN API #
############

###################################################################################################
# Imports
from fastapi import FastAPI, status
from app.db.database import create_db_and_tables
from app.models import characters, powers, character_power
from app.routers import characters, powers, character_power
###################################################################################################


###################################################################################################
# API configuration
app = FastAPI()
###################################################################################################


###################################################################################################
# Models initialization
@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
###################################################################################################


###################################################################################################
# Router connection
app.include_router(characters.router)
app.include_router(powers.router)
app.include_router(character_power.router)
###################################################################################################


###################################################################################################
# Welcome message
@app.get(
        "/", 
        summary="Welcome message", 
        tags=["Welcome"],
        responses={
            status.HTTP_200_OK:{
                "description": "Successful Response",
                "content":{
                    "application/json": {
                        "example": {
                            "message": "Welcome to Heroes and Villains API!"
                        }
                    }
                }
            }
        }
)
async def welcome():
    
    """ Welcome to the API!
    """
    
    return {"message": "Welcome to Heroes and Villains API!"}
###################################################################################################