####################
# Character's CRUD #
####################


###################################################################################################
# Imports
from typing import Annotated
from sqlmodel import Session, select
from pydantic import ValidationError
from app.models.characters import Character
###################################################################################################

###################################################################################################
###################################################################################################
class CharacterCrud():

    ###############################################################################################
    # Create
    @staticmethod
    def create_character(*, session: Session, character: Character):
        """
            Method to create new characters

            :param Session session: database session
            :param Character character: Object Character
            :return: The created Character
        """
        session.add(character)
        session.commit()
        session.refresh(character)
        return character
    ###############################################################################################


    ###############################################################################################
    # Read
    @staticmethod
    def read_characters(
        *, 
        session: Session, 
        character_id: int | None = None,
        offset: int | None = None,
        limit: int | None = None
    ):
        """
            Method to read characters in database. Returns one character if
            a character_id is provided

            :param Session session: database session
            :param int character_id: the character's ID
            :param int offset: an integer parameter for pagination
            :param int limit: the maximum number of characters returned
            :return: a list of characters or a character
        """
        if not character_id:
            query = select(Character).offset(offset).limit(limit)
            result = session.exec(query).all()
        
        else:
            query = select(Character).where(Character.character_id == character_id)
            result = session.exec(query).first()

        return result
    ###############################################################################################


    ###############################################################################################
    @staticmethod
    def update_character(
        *, 
        session: Session, 
        character_id: int, 
        args: dict
    ):
        '''
            Method to update an existing character
            
            :param Session session: database session
            :param int character_id: the character's ID
            :param dict args: a dict with the Character fields to be updated
            :return: the updated character
        '''
        character_update = session.get(Character, character_id)

        if not character_update:
            return None

        if "name" in args:
            character_update.name = args['name']
        if "secret_name" in args:
            character_update.secret_name = args["secret_name"]
        if "age" in args:
            character_update.age = args["age"]
        
        session.add(character_update)
        session.commit()
        session.refresh(character_update)

        return character_update
    ###############################################################################################

    
    ###############################################################################################
    @staticmethod
    def delete_character(
        *,
        session: Session,
        character_id: int
    ):
        '''
            Method to delete a character

            :param Session session: database session
            :param int character_id: the character's ID
            :return: the deleted character
        '''

        character_delete = session.get(Character, character_id)

        if not character_delete:
            return None
        
        session.delete(character_delete)
        session.commit()
        
        return character_delete
    ###############################################################################################


    ###############################################################################################
    @staticmethod
    def get_heroes_or_villains(
        session: Session,
        character_type: str
    ) -> list[Character] | None:
        
        """
            Method to return all the heroes or all the villains from the database by passing the
            character_type.

            :param str character_type: the character's category (hero or villain)
            :return: a list of Character or None
        """

        ## Validate the character type
        if character_type not in ('hero', 'villain'):
            return None
        
        # Get the heroes or villains
        result = session.exec(
            select(Character).where(Character.character_type == character_type)
        ).all()

        # Return the result
        return result
    ###############################################################################################

###################################################################################################
###################################################################################################