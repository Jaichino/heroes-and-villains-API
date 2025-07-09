#######################
# CharacterPower CRUD #
#######################

###################################################################################################
# Imports
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.models.character_power import CharacterPower
from app.models.characters import Character
from app.models.powers import Powers

###################################################################################################

class CharacterPowerCrud:

##################################################################################################
# Create
    @staticmethod
    def assign_power_to_character(
        session: Session,
        character_id: int,
        power_id: int
    ) -> bool | None:
        
        """ Method to give a power to a character by passing the character_id and the
            power_id

            :param Session session: database session
            :param int character_id: the character's id
            :param int power_id: the power's id
            :return: True if the power was assigned, False if there was an IntegrityError
        """

        # Verify that the character and the power exist
        character = session.get(Character, character_id)
        power = session.get(Powers, power_id)

        # Return None if the character or the power doesn't exist
        if not character or not power:
            return None
        
        # Assign the power to the character
        try:
            link = CharacterPower(character_id=character_id, power_id=power_id)
            session.add(link)
            session.commit()
            return True
        
        except IntegrityError:
            session.rollback()
            return False
##################################################################################################


##################################################################################################
# Read
    @staticmethod
    def read_characters_powers(session: Session, character_id: int)-> list[Powers]:

        """ Method to return a list of a charater's powers by passing the character's ID

            :param Session session: database session
            :param int character_id: the character's ID
            :return: a list of objects Powers
        """
        
        # Get the character
        character = session.get(Character, character_id)

        # If character is None, then return None
        if not character:
            return None
        
        # Get the character's powers
        character_powers = character.powers

        # Return the character's powers
        return character_powers
##################################################################################################


##################################################################################################
# Delete
    @staticmethod
    def delete_character_power(
        session: Session,
        character_id: int,
        power_id: int
    ) -> bool:
        
        """ Method to delete a power of a character by passing the character_id and power_id

            :param Session session: database session
            :param int character_id: the character's id
            :param int power_id: the id of the power to be deleted from the character
        """

        # Get the character and the power
        statement = (
            select(CharacterPower)
            .where(
                CharacterPower.character_id == character_id,
                CharacterPower.power_id == power_id
            )
        )
        character_power = session.exec(statement).first()

        # If character_power is None, then return False (character or power not found)
        if character_power is None:
            return False
        
        # Delete the power from the character
        session.delete(character_power)
        session.commit()

        # Returns True if the power has been deleted
        return True