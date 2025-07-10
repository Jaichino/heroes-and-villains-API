###############################################
# API Router to handle the character's powers #
###############################################

###################################################################################################
# Imports
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from app.db.database import get_session
from app.crud.character_power import CharacterPowerCrud
from app.models.powers import PowerPublic, Powers
from app.models.characters import Character
###################################################################################################


###################################################################################################
# Router configuration
router = APIRouter(
    prefix="/characters/{character_id}/powers",
    tags=["Character's Powers"]
)
###################################################################################################


###################################################################################################
# Session dependency
SessionDep = Annotated[Session, Depends(get_session)]
###################################################################################################


###################################################################################################
# Assign powers endpoint
@router.post(
    "/{power_id}",
    summary="Assign a power to a character",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Created",
            "content": {
                "application/json":{
                    "example":{
                        "message":"Power successfully assigned to the character!"
                    }
                }
            }
        },
        status.HTTP_409_CONFLICT: {
            "description": "Conflict",
            "content":{
                "application/json":{
                    "example":{
                        "detail":"Power already assigned to the character!"
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content":{
                "application/json":{
                    "example":{
                        "detail":"Character or power not found!"
                    }
                }
            }
        }
    }
)
async def assing_power(
    session: SessionDep,
    character_id: int,
    power_id: int
) -> JSONResponse:
    
    """ Function to assign a power to a character by passing the character_id
        and power_id

        - **character_id**: the character's id
        - **power_id**: the power's id to be assigned to the character
    """

    # Assign the power
    power_assigned = CharacterPowerCrud.assign_power_to_character(
        session=session,
        character_id=character_id,
        power_id=power_id
    )

    # Verify the response
    if power_assigned is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Power already assigned to the character!"
        )
    
    if power_assigned is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character or power not found!"
        )
    
    return JSONResponse(content={
        "message":"Power successfully assigned to the character!"
    })
###################################################################################################


###################################################################################################
# Read character's powers endpoint
@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "description": "Successful Response",
            "content": {
                "application/json":{
                    "example": {
                        "character": {
                        "character_id": 11,
                        "character_name": "Spiderman"
                        },
                        "powers": [
                            {
                                "power_damage": 320,
                                "power_id": 7,
                                "power_name": "Web Shooting"
                            }
                        ]
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
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
async def read_characters_powers(
    session: SessionDep,
    character_id: int
) -> JSONResponse:
    
    """ Function to return the list of powers of a character by passing
        the character's ID.

        - **character_id**: the character's ID
    """

    # Get the powers
    powers = CharacterPowerCrud.read_characters_powers(
        session=session,
        character_id=character_id
    )

    # Raise 404 if powers returns None (couldn't find the character)
    if powers is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found!"
        )
    
    # Get the character
    character = session.get(Character, character_id)
    
    # Return the powers
    return JSONResponse(
        content={
            "character": {
                "character_id": character.character_id,
                "character_name": character.name
            },
            "powers": jsonable_encoder(powers)
        }
    )
###################################################################################################


###################################################################################################
# Endpoint to delete a character's power
@router.delete(
    "/{power_id}",
    summary="Delete a character's power",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_202_ACCEPTED: {
            "description": "Accepted",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Power successfully removed from the character!",
                        "deleted_power": {
                            "power_name": "Super Strenght",
                            "power_damage": 400,
                            "power_id": 6
                        },
                        "deleted_from": {
                            "character_name": "Captain America",
                            "character_id": 3
                        }
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {"detail": "Couldn't get the character or the power"}
                }
            }
        }
    }
)
async def delete_character_power(
    session: SessionDep,
    character_id: int,
    power_id: int
) -> JSONResponse:
    
    """ Function to delete a power from a character by passing the character's ID and
        the power's ID.

        - **character_id**: the character's ID
        - **power_id**: the power's ID
    """

    # Remove the power from the character
    remove_power = CharacterPowerCrud.delete_character_power(
        session=session,
        character_id=character_id,
        power_id=power_id
    )

    # Raise a 404 if remove_power is False (couldn't get the character or power)
    if remove_power is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Couldn't get the character or the power"
        )
    
    # Get the deleted power
    deleted_power = session.get(Powers, power_id)
    # Get the character
    character = session.get(Character, character_id)

    # Verify if the power or character exists
    if not deleted_power or not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Couldn't get the character or the power"
        )

    # Response
    response = JSONResponse(
        content={
            "message": "Power successfully removed from the character!",
            "deleted_power": jsonable_encoder(deleted_power),
            "deleted_from": {
                "character_name": character.name,
                "character_id": character_id
            }
        }
    )

    return response