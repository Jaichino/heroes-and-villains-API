# Fichero para contener la lógica de Heroes

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.db.database import get_session
from app.models.heroes import HeroCreate, HeroPublic, HeroUpdate, Hero
from app.crud.heroes import HeroCrud


# Configuración del router
router = APIRouter(
    prefix="/heroes",
    tags=["Heroes"]
)

SessionDep = Annotated[Session, Depends(get_session)]

# Creación de un nuevo heroe
@router.post("/")
async def create_hero(
    session: SessionDep,
    hero: HeroCreate
):
    db_hero = Hero.model_validate(hero)
    db_hero = HeroCrud.create_hero(session=session, hero=db_hero)
    return db_hero


# Lectura de heroes
@router.get("/", response_model=list[HeroPublic])
async def read_heroes(
    session: SessionDep
):
    heroes = HeroCrud.read_heroes(session=session, hero_id=None)
    return heroes


@router.get("/{hero_id}", response_model=HeroPublic)
async def read_hero_id(
    session: SessionDep,
    hero_id: int
):
    heroe = HeroCrud.read_heroes(session=session, hero_id=hero_id)
    if not heroe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found!"
        )
    
    return heroe


# Actualización de heroes
@router.patch("/{hero_id}", response_model=HeroPublic)
async def update_hero(
    session: SessionDep,
    hero_id: int,
    hero_update: HeroUpdate 
):

    # Transformación de objeto HeroUpdate en diccionario
    heroe_dict = hero_update.model_dump(exclude_unset=True)

    # Actualización del heroe
    response = HeroCrud.update_hero(
        session=session,
        hero_id=hero_id,
        args=heroe_dict
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found!"
        )
    
    return response


# Eliminación de heroes
@router.delete("/{hero_id}", response_model=HeroPublic)
async def delete_hero(
    session: SessionDep,
    hero_id: int
):
    response = HeroCrud.delete_hero(
        session=session,
        hero_id=hero_id
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Hero not found!"
        )
    
    return response