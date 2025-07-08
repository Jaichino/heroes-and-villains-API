#############################
# API Router for Characters #
#############################


###################################################################################################
# Imports
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body
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
# Character create endpoint
@router.post(
        "/", 
        response_model=CharacterPublic, 
        summary="Create a new character",
        status_code=status.HTTP_201_CREATED,
        responses={
            status.HTTP_201_CREATED:{
                "description":"Character successfully created!",
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
    """ Function to create a new character with a JSON body with the following
        parameters:

        - **name**: character's name
        - **secret_name** (opt): character's secret name
        - **age** (opt): character's age
        - **character_type**: character's category (Hero or Villain)
    """
    # Model validation for CharacterCreate
    db_character = Character.model_validate(character)

    # Create and return the character
    db_character = CharacterCrud.create_character(session=session, character=db_character)
    return db_character
###################################################################################################


###################################################################################################
# Characters read endpoints
@router.get("/", response_model=list[CharacterPublic], summary="Get all the characters")
async def read_characters(
    session: SessionDep
):
    """
        Function to return all the characters in the database
    """
    # Get and return all the characters
    characters = CharacterCrud.read_characters(session=session, character_id=None)
    return characters


@router.get("/{character_id}", response_model=CharacterPublic, summary="Get one character")
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
    if not character_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found!"
        )
    
    # Return the character
    return character
###################################################################################################


###################################################################################################
# Character update endpoint
@router.patch(
        "/{character_id}", 
        response_model=CharacterPublic, 
        summary="Update a character",
        responses={
            status.HTTP_200_OK: {
                "description": "Character successfully updated!"
            }
        }
)
async def update_character(
    session: SessionDep,
    character_id: int,
    character_update: Annotated[
        CharacterUpdate,
        Body(example={
            "secret_name":"Steve",
            "age": 100,
        })
    ] 
):
    """ Function to update a character by passing their ID and a JSON body
        with the fields to be modified

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
        summary="Delete a character",
        responses={
            status.HTTP_202_ACCEPTED:{
                "description":"Character successfully deleted!",
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
                "description":"Character not found!",
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
):
    """
        Function to delete a character by passing their ID.

        - **character_id**: character's ID
    """
    # Delete the character
    response = CharacterCrud.delete_character(
        session=session,
        character_id=character_id
    )

    # If delete_character returns None, raise a 404 not found status code
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Character not found!"
        )
    
    # Return the deleted character
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=jsonable_encoder(response)
    )
###################################################################################################