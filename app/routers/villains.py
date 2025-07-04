from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session
from app.models.villains import VillainCreate, VillainPublic, VillainUpdate, Villain
from app.db.database import get_session
from app.crud.villains import VillainCrud

router = APIRouter(
    prefix="/villains",
    tags=["Villains"]
)

SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/", response_model=VillainPublic, summary='Function to create new villains')
async def create_villain(
    session: SessionDep,
    villain: Annotated[
        VillainCreate, 
        Body(example={
            "evil_name": "Thanos",
            "secret_name": "El pera de escroto",
            "age": 65
        })]
):
    """ Function to create new villains with the following params:

        - **evil_name**: villain's name
        - **secret_name**: villain's secret name
        - **age**: villain's age
    """
    
    villain_db = Villain.model_validate(villain)
    villain_db = VillainCrud.create_villain(session=session, villain=villain_db)

    return villain_db

