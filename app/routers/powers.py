#############################
#   API Router for Powers   #
#############################

###################################################################################################
# Imports
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlmodel import Session
from app.db.database import engine, get_session
from app.models.powers import Powers, PowerCreate, PowerPublic, PowerUpdate
from app.crud.powers import PowersCrud
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
# Power create endpoint
@router.post(
    "/",
    response_model=PowerPublic,
    summary="Create a new power",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Power successfully created!",
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
    
    """ Function to create a new power by passing a PowerCreate JSON body with
        the fields:

        - **power_name (str)**: the power's name
        - **power_damage (int)**: the power's damage (between 0 and 1000)
    """

    # Validate the PowerCreate model
    power_db = Powers.model_validate(power)

    # Create the power and return it
    power_create = PowersCrud.create_power(session=session, power=power_db)

    return power_create


###################################################################################################
# Update power endpoint
@router.patch(
    "/{power_id}",
    response_model=PowerPublic,
    status_code=status.HTTP_200_OK,
    summary="Update a power",
    responses={
        200: {
            "description": "Power successfully updated!",
            "content": {
                "application/json":{
                    "example": {
                        "power_name": "Time manipulation 2.0",
                        "power_damage": 150
                    }
                }
            }
        },

        404: {
            "description": "Power not found!",
            "content":{
                "application/json":{
                    "example":{"detail":"Power not found"}
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
):
    """ Function to update a power by passing its power_id and a PowerUpdate JSON body
        with the fields to be modified.

        - **power_id (int)**: the power's ID
        - **power_update**: a PowerUpdate object with the following optional fields:

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

    # Raise an exception if update_power returns None
    if power_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Power with ID={power_id} not found!"
        )
    
    # Return the updated power
    return power_to_update
###################################################################################################


###################################################################################################
# Delete power endpoint
@router.delete(
    "/{power_id}",
    response_model=PowerPublic,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete a power",
    responses={
        202: {  "description": "Power successfully deleted",
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
        404: {
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


