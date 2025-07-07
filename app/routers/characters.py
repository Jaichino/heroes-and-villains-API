#############################
# API Router for Characters #
#############################

# Imports

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.db.database import get_session
from app.models.characters import CharacterCreate, CharacterPublic, CharacterUpdate, Character
from app.crud.characters import CharacterCrud


# Router configuration
router = APIRouter(
    prefix="/characters",
    tags=["Characters"]
)

# Session dependency
SessionDep = Annotated[Session, Depends(get_session)]


# Character create endpoint
@router.post("/")
async def create_character(
    session: SessionDep,
    character: CharacterCreate
):
    # Model validation for CharacterCreate
    db_character = Character.model_validate(character)

    # Create and return the character
    db_character = CharacterCrud.create_character(session=session, character=db_character)
    return db_character


# Characters read endpoints
@router.get("/", response_model=list[CharacterPublic])
async def read_characters(
    session: SessionDep
):
    # Get and return all the characters
    characters = CharacterCrud.read_characters(session=session, character_id=None)
    return characters


@router.get("/{character_id}", response_model=CharacterPublic)
async def read_character_id(
    session: SessionDep,
    character_id: int
):
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


# Character update endpoint
@router.patch("/{character_id}", response_model=CharacterPublic)
async def update_character(
    session: SessionDep,
    character_id: int,
    character_update: CharacterUpdate 
):

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


# Character delete endopoint
@router.delete("/{character_id}", response_model=CharacterPublic)
async def delete_character(
    session: SessionDep,
    character_id: int
):
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
    return response