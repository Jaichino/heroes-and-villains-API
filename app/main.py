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
description = """
This API allows you to do the following things:

### Characters

You will be able to:

* **Create new characters**: You can create heroes and villains
* **Read existing characters**: You can get all the characters or only one of them
* **Update character's properties**: You can update any of the character's attributes
* **Delete characters**: You can also delete a character

### Powers

This section allows you to:

* **Create new powers**: You can create new powers with their respective damages
* **Read powers**: You can get all the powers or only one.
* **Update powers**: You can update any of the power's attributes
* **Delete powers**: You can delete powers

### Character's Powers

And here, you can:

* **Asign a power** to a character
* **Read the powers** of a certain character
* **Delete a power** of a certain character
"""

app = FastAPI(
    title="Heroes and Villains API",
    summary="RESTful API built with FastAPI for managing heroes and villains",
    description=description,
    contact={"name": "Aichino, Juan", "email": "aichinojuani@gmail.com"}
)

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