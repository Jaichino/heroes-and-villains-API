#############################
#   API Router for Powers   #
#############################

###################################################################################################
# Imports
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Body, Query
from sqlmodel import Session
from app.db.database import engine, get_session
from app.models.powers import Powers, PowerCreate, PowerPublic, PowerUpdate
from app.crud.powers import PowersCrud
from app.auth.auth import get_current_user
###################################################################################################


###################################################################################################
# Router configuration
router = APIRouter(
    prefix="/powers",
    tags=["Powers"]
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
# Endpoint to create new powers
@router.post(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=PowerPublic,
    summary="Create a new power",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Accepted",
            "content":{
                "application/json":{
                    "example":{
                        "power_name": "Time Manipulation",
                        "power_damage": 100,
                        "power_id": 0
                    }
                }
            }
        }
    }
)
async def create_power(
    session: SessionDep,
    power: Annotated[
        PowerCreate,
        Body(
            example={
            "power_name": "Time Manipulation",
            "power_damage": 100
            }
        )
    ]
) -> PowerPublic:
    
    """ Function to create a new power by passing a JSON body with the following
        fields:

        - **power_name (str)**: the power's name
        - **power_damage (int)**: the power's damage (between 0 and 1000)
    """

    # Validate the PowerCreate (power) model
    power_db = Powers.model_validate(power)

    # Create the power and return it
    power_create = PowersCrud.create_power(session=session, power=power_db)

    return power_create
###################################################################################################


###################################################################################################
# Endpoint to get all the powers
@router.get(
        "/",
        response_model=list[PowerPublic],
        status_code=status.HTTP_200_OK,
        summary="Get the powers",
        responses= {
            status.HTTP_200_OK: {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "power_name": "Time Manipulation",
                                "power_damage": 100,
                                "power_id": 3
                            },
                            {
                                "power_name": "Repulsor Blast",
                                "power_damage": 250,
                                "power_id": 5
                            }
                        ]
                    }
                }
            }
        }
)
async def read_all_powers(
    session: SessionDep,
    offset: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10
) -> list[PowerPublic]:
    
    """ Function to get the powers from the database, with optional query parameters offset and
        limit.

        - **offset**: int query parameter for pagination (default = 0)
        - **limit**: the maximum number of powers returned (default = 10)
    """

    # Get the powers and return them
    powers = PowersCrud.read_powers(
        session=session,
        power_id = None,
        offset=offset,
        limit=limit
    )

    return powers


# Endpoint to get only one power
@router.get(
        "/{power_id}",
        response_model=PowerPublic,
        summary="Get one power",
        responses={
            status.HTTP_200_OK: {
                "content": {
                    "application/json": {
                        "example": {
                            "power_name": "Time Manipulation",
                            "power_damage": 100,
                            "power_id": 3
                        }
                    }
                }
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "Not Found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Couldn't get the power with the given power_id"
                        }
                    }
                }
            }
        }
)
async def get_one_power(
    session: SessionDep,
    power_id: int
) -> PowerPublic:
    
    """ Function to get only one power by passing its power_id

        - **power_id**: the power's ID
    """

    # Get the power
    power = PowersCrud.read_powers(
        session=session,
        power_id=power_id
    )

    # Raise 404 if the power is None (couldn't get the power with power_id)
    if power is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Couldn't get the power with the given power_id"
        )

    # Return the power
    return power
###################################################################################################


###################################################################################################
# Endpoint to update powers
@router.patch(
    "/{power_id}",
    response_model=PowerPublic,
    status_code=status.HTTP_200_OK,
    summary="Update a power",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json":{
                    "example": {
                        "power_name": "Time manipulation 2.0",
                        "power_damage": 150
                    }
                }
            }
        },

        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content":{
                "application/json":{
                    "example": {"detail":"Power not found"}
                }
            }
        }
    }
)
async def update_power(
    session: SessionDep,
    power_id: int,
    power_update: Annotated[
        PowerUpdate,
        Body(
            example={
                "power_name": "Time Manipulation 2.0",
                "power_damage": 150
            }
        )
    ]
) -> PowerPublic:
    
    """ Function to update a power by passing its power_id and a JSON body
        with the fields to be modified.

        - **power_id (int)**: the power's ID
        - **power_update**: Request body with the fields:

            - *power_name (str)*: the power's name
            - *power_damage (int)*: the power's damage 
    """

    # Get a dict with only the client's given fields
    power_update_dict = power_update.model_dump(exclude_unset=True)

    # Update the power
    power_to_update = PowersCrud.update_power(
        session=session,
        power_id=power_id,
        power_update=power_update_dict
    )

    # Raise an exception if power_to_update is None
    if power_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Power not found!"
        )
    
    # Return the updated power
    return power_to_update
###################################################################################################


###################################################################################################
# Endpoint to delete a power
@router.delete(
    "/{power_id}",
    dependencies=[Depends(get_current_user)],
    response_model=PowerPublic,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete a power",
    responses={
        status.HTTP_202_ACCEPTED: {  "description": "Accepted",
                "content": {
                    "application/json": {
                        "example": {
                            "power_name": "Time Manipulation",
                            "power_damage": 100,
                            "power_id": 3
                        }
                    }
                }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content":{
                "application/json":{
                    "example": {
                        "detail":"Power not found!"
                    }
                }
            }
        }
    }
)
async def delete_power(
    session: SessionDep,
    power_id: int
) -> PowerPublic:
    
    """ Function to delete a power by passing its power_id

        - **power_id (int)**: the power's ID
    """

    # Delete the power
    power_deleted = PowersCrud.delete_power(session=session, power_id=power_id)
    
    # Raise an exception if delete_power returns None
    if power_deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Power not found!"
        )

    # Return the deleted power
    return power_deleted


