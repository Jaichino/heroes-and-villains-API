#############################
# API Router for Characters #
#############################


###################################################################################################
# Imports
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.db.database import get_session
from app.models.characters import CharacterCreate, CharacterPublic, CharacterUpdate, Character
from app.crud.characters import CharacterCrud
####################################################################################################


###################################################################################################
# Router configuration
router = APIRouter(
    prefix="/characters",
    tags=["Characters"]
)
###################################################################################################


###################################################################################################
# Session dependency
SessionDep = Annotated[Session, Depends(get_session)]
###################################################################################################


###################################################################################################
# Endpoints
###################################################################################################

###################################################################################################
# Endpoint to create new characters
@router.post(
        "/", 
        response_model=CharacterPublic, 
        summary="Create a new character",
        status_code=status.HTTP_201_CREATED,
        responses={
            status.HTTP_201_CREATED:{
                "description":"Created",
                "content":{
                    "application/json":{
                        "example":{
                            "name": "Captain America",
                            "secret_name":"Steve",
                            "age": 100,
                            "character_type": "Hero",
                            "character_id": 3
                        }
                    }
                }
            }
        }
)
async def create_character(
    session: SessionDep,
    character: Annotated[
        CharacterCreate, 
        Body(example={
            "name":"Captain America",
            "secret_name": "Steve Rogers",
            "age": 105,
            "character_type": "Hero"
        })
    ]
):
    """ Function to create a new character by passsing a JSON body with the following
        parameters:

        - **name**: character's name
        - **secret_name** (opt): character's secret name
        - **age** (opt): character's age
        - **character_type**: character's category (Hero or Villain)
    """
    # Model validation for CharacterCreate (character)
    db_character = Character.model_validate(character)

    # Create and return the character
    db_character = CharacterCrud.create_character(session=session, character=db_character)
    return db_character
###################################################################################################


###################################################################################################
# Endpoints to read characters

# Get all the characters (with offset and limit query parameters)
@router.get(
        "/", 
        response_model=list[CharacterPublic], 
        summary="Get all the characters",
        responses={
            status.HTTP_200_OK: {
                "content":{
                    "application/json":{
                        "example": [{
                            "name": "Captain America",
                            "secret_name": "Steve Rogers",
                            "age": 105,
                            "character_type": "Hero",
                            "character_id": 3
                        },
                        {
                            "name": "Iron Man",
                            "secret_name": "Tony Stark",
                            "age": 36,
                            "character_type": "Hero",
                            "character_id": 1
                        }]
                    }
                }
            }
        }
)

async def read_characters(
    session: SessionDep,
    offset: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10
):
    """
        Function to return all the characters in the database with the optional query
        parameters offset and limit for pagination. The limit parameter is setted in
        10 by default, and the offset is setted in 0.

        - **offset**: int query param for pagination
        - **limit**: the maximum quantity of characters returned
    """
    # Get and return the characters
    characters = CharacterCrud.read_characters(
        session=session, 
        character_id=None,
        offset=offset,
        limit=limit
    )

    return characters


# Get one character
@router.get(
        "/{character_id}", 
        response_model=CharacterPublic, 
        summary="Get one character",
        responses={
            status.HTTP_200_OK: {
                "content": {
                    "application/json": {
                        "example": {
                            "name": "Captain America",
                            "secret_name": "Steve Rogers",
                            "age": 105,
                            "character_type": "Hero",
                            "character_id": 3
                        }
                    }
                }
            },
            status.HTTP_404_NOT_FOUND: {
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Character not found!"
                        }
                    }
                }
            }
        }
)
async def read_character_id(
    session: SessionDep,
    character_id: int
):
    """ Function to return one character by passing their character_id

        - **character_id**: character's ID.
    """

    # Get the character
    character = CharacterCrud.read_characters(session=session, character_id=character_id)
    
    # If read_characters returns None, raise a 404 not found status code
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found!"
        )
    
    # Return the character
    return character


# Get all the heroes or all the villains
@router.get(
        "/type/{character_type}",
        summary="Get all the heroes or all the villains",
        response_model=list[CharacterPublic],
        response_model_exclude_none=True,
        responses={
            status.HTTP_200_OK: {
                "content": {
                    "application/json": {
                        "example": [{
                            "name": "Thanos",
                            "secret_name": None,
                            "age": None,
                            "character_type": "Villain",
                            "character_id": 13
                        },
                        {
                            "name": "Venom",
                            "secret_name": "Eddie Brock",
                            "age": 38,
                            "character_type": "Villain",
                            "character_id": 14
                        }]
                    }
                }
            }
        }
)
async def getall_heroes_or_villains(
    session: SessionDep,
    character_type: str,
    offset: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10
) -> list[CharacterPublic]:
    
    """ Function to return all the heroes or all the villains from the database by passing the
        parameter character_type.
        Offset and limit query parameters allow pagination  and limiting the number of records.

        - **character_type**: the clasification of the character (hero or villain)
        - **offset**: int query parameter to allow pagination (default 0)
        - **limit**: the maximum quantity of characters returned (default 10)
    """

    # Get the heroes or villains and return them
    characters = CharacterCrud.get_heroes_or_villains(
        session=session, 
        character_type=character_type,
        offset=offset,
        limit=limit
    )

    if characters is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="character_type must be 'hero' or 'villain'"
        )

    return characters
###################################################################################################


###################################################################################################
# Endpoint to update a character
@router.patch(
        "/{character_id}", 
        response_model=CharacterPublic, 
        summary="Update a character",
        response_model_exclude_none=True,
        responses={
            status.HTTP_200_OK: {
                "content": {
                    "application/json": {
                        "example": {
                            "name": "Thanos",
                            "secret_name": None,
                            "age": 65,
                            "character_type": "Villain",
                            "character_id": 13
                        }
                    }
                }
            }
        }
)
async def update_character(
    session: SessionDep,
    character_id: int,
    character_update: Annotated[
        CharacterUpdate,
        Body(example={
            "age": 65,
        })
    ] 
):
    """ Function to update a character by passing their ID and a JSON body
        with only the fields to be modified.

        - **character_id**: character's ID.

        - **character_update**: JSON body with the fields to be modified:
            - **name** (opt): new character's name
            - **secret_name** (opt): new character's secret name
            - **age** (opt): new character's age
            - **character_type** (opt): new character's type (Hero or Villain)
    """ 

    # Create a dict with character_update object
    character_dict = character_update.model_dump(exclude_unset=True)

    # Update the character
    response = CharacterCrud.update_character(
        session=session,
        character_id=character_id,
        args=character_dict
    )

    # If update_character returns None, raise 404 not found
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found!"
        )
    
    # Return the updated character
    return response
###################################################################################################


###################################################################################################
# Character delete endopoint
@router.delete(
        "/{character_id}", 
        response_model=CharacterPublic,
        status_code=status.HTTP_202_ACCEPTED,
        response_model_exclude_none=True,
        summary="Delete a character",
        responses={
            status.HTTP_202_ACCEPTED:{
                "description": "Accepted",
                "content":{
                    "application/json":{
                        "example":{
                            "name": "Ultron",
                            "secret_name": None,
                            "age": None,
                            "character_type": "Villain",
                            "character_id": 0
                        }
                    }
                }},
            status.HTTP_404_NOT_FOUND:{
                "content":{
                    "application/json":{
                        "example":{
                            "detail":"Character not found!"
                        }
                    }
                }}
        }
)
async def delete_character(
    session: SessionDep,
    character_id: int
) -> CharacterPublic:
    
    """
        Function to delete a character by passing their ID.

        - **character_id**: character's ID
    """
    # Delete the character
    deleted_character = CharacterCrud.delete_character(
        session=session,
        character_id=character_id
    )

    # If delete_character returns None, raise a 404 not found status code
    if deleted_character is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Character not found!"
        )
    
    # Return the deleted character
    return deleted_character
###################################################################################################

###################################################################################################