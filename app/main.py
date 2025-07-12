############
# MAIN API #
############

###################################################################################################
# Imports
from fastapi import FastAPI, status
from app.db.database import create_db_and_tables
from app.models import characters, powers, character_power, users
from app.routers import characters, powers, character_power, admin, login
###################################################################################################


###################################################################################################
# API configuration
description = """
This API allows you to manage a universe of heroes and villains, their powers, and the relationships 
between them.

### Security

The API implements authentication using OAuth2 Password Bearer with JWT tokens.
Endpoints that modify data (i.e., POST and DELETE) are protected and require a valid token to access.

### Characters

You can:

* **Create new characters**: Add new heroes or villains to the database.
* **Read existing characters**: Get a list of all characters or fetch a specific one by ID.
* **Update character's properties**: Modify the attributes of any character.
* **Delete characters**: Remove characters from the database.

### Powers

You can:

* **Create new powers**: Add new abilities with their corresponding damage values.
* **Read powers**:  Get a list of all powers or fetch a specific one by ID.
* **Update powers**: Modify power attributes such as name or damage.
* **Delete powers**: Remove powers from the database.

### Character Powers

You can:

* **Asign a power**: Link an existing power to a character.
* **Read the powers**: View all powers associated with a specific character.
* **Delete a power**: Detach a power from a character.
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
app.include_router(admin.router)
app.include_router(login.router)
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