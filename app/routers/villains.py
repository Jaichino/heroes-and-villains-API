# Imports
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session
from app.models.villains import VillainCreate, VillainPublic, VillainUpdate, Villain
from app.db.database import get_session
from app.crud.villains import VillainCrud

# Router configuration
router = APIRouter(
    prefix="/villains",
    tags=["Villains"]
)

# Session dependency
SessionDep = Annotated[Session, Depends(get_session)]


# Villains creation endpoint
@router.post("/", response_model=VillainPublic, summary='Create new villains')
async def create_villain(
    session: SessionDep,
    villain: Annotated[
        VillainCreate, 
        Body(example={
            "evil_name": "Loki",
            "secret_name": "Loki Laufeyson",
            "age": 1059
        })]
):
    """ Function to create new villains with a JSON body with the following parameters:

        - **evil_name**: villain's name
        - **secret_name**: villain's secret name
        - **age**: villain's age
    """
    
    villain_db = Villain.model_validate(villain)
    villain_db = VillainCrud.create_villain(session=session, villain=villain_db)

    return villain_db


# Villains get endpoints
@router.get("/", response_model=list[VillainPublic], summary='Get all the villains')
async def get_villains(
    session: SessionDep
):
    ''' Function to return all the villains in the database
    '''
    villains = VillainCrud.read_villains(session=session, villain_id=None)

    return villains


@router.get("/{villain_id}", response_model=Villain, summary='Get one villain')
async def get_one_villain(
    session: SessionDep,
    villain_id: int
):
    """ Function to return a villain with their id.

        - **villain_id**: Villain's ID. (int)
    """

    villain = VillainCrud.read_villains(session=session, villain_id=villain_id)

    if not villain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Villain with id={villain_id} not found!'
        )
    
    return villain


# Villain update endpoint
@router.patch("/{villain_id}", response_model=VillainPublic, summary="Update a villain")
async def update_villain(
    session: SessionDep,
    villain_id: int,
    villain: VillainUpdate
):
    """
        Function to update a villain with their ID.

        - **villain_id**: Villain's ID
        - **villain**: JSON with the fields to be updated
    """
    # Dict with user-configured attributes 
    villain_dict = villain.model_dump(exclude_unset=True)

    # Update the villain
    villain_update = VillainCrud.update_villain(
        session=session,
        villain_id=villain_id,
        villain=villain_dict
    )

    # Raise 404 if the villain is not found
    if villain_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Villain with ID={villain_id} not found!"
        )
    
    # Return the updated villain
    return villain_update


# Villain delete endpoint
@router.delete("/{villain_id}", response_model=VillainPublic, summary="Delete a villain")
async def delete_villain(
    session: SessionDep,
    villain_id: int
):
    """ Function to delete a villain with their ID

        - **villain_id**: Villain's ID (int)
    """
    # Delete the villain
    villain_delete = VillainCrud.delete_villain(session=session, villain_id=villain_id)

    # If villain_delete = None, raise 404 status code
    if villain_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Villain with ID={villain_id} not found!"
        )
    
    return villain_delete