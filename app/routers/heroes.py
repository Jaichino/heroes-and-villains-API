#########################
# API Router for Heroes #
#########################

# Imports

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.db.database import get_session
from app.models.heroes import HeroCreate, HeroPublic, HeroUpdate, Hero
from app.crud.heroes import HeroCrud


# Router configuration
router = APIRouter(
    prefix="/heroes",
    tags=["Heroes"]
)

# Session dependency
SessionDep = Annotated[Session, Depends(get_session)]


# Heroe create endpoint
@router.post("/")
async def create_hero(
    session: SessionDep,
    hero: HeroCreate
):
    # Model validation for HeroCreate
    db_hero = Hero.model_validate(hero)

    # Create and return the hero
    db_hero = HeroCrud.create_hero(session=session, hero=db_hero)
    return db_hero


# Heroes read endpoints
@router.get("/", response_model=list[HeroPublic])
async def read_heroes(
    session: SessionDep
):
    # Get and return the heroes
    heroes = HeroCrud.read_heroes(session=session, hero_id=None)
    return heroes


@router.get("/{hero_id}", response_model=HeroPublic)
async def read_hero_id(
    session: SessionDep,
    hero_id: int
):
    # Get the heroe
    heroe = HeroCrud.read_heroes(session=session, hero_id=hero_id)
    
    # If read_heroes returns None, raise a 404 not found status code
    if not heroe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found!"
        )
    
    # Return the hero
    return heroe


# Hero update endpoint
@router.patch("/{hero_id}", response_model=HeroPublic)
async def update_hero(
    session: SessionDep,
    hero_id: int,
    hero_update: HeroUpdate 
):

    # Create a dict with hero_update object
    heroe_dict = hero_update.model_dump(exclude_unset=True)

    # Update the hero
    response = HeroCrud.update_hero(
        session=session,
        hero_id=hero_id,
        args=heroe_dict
    )

    # If update_hero returns None, raise 404 not found
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found!"
        )
    
    # Return the updated hero
    return response


# Eliminación de heroes
@router.delete("/{hero_id}", response_model=HeroPublic)
async def delete_hero(
    session: SessionDep,
    hero_id: int
):
    # Delete the hero
    response = HeroCrud.delete_hero(
        session=session,
        hero_id=hero_id
    )

    # If delete_hero returns None, raise a 404 not found status code
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Hero not found!"
        )
    
    # Return the deleted hero
    return response