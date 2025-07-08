####################
#   Power's CRUD   #
####################

###################################################################################################
# Imports
from sqlmodel import Session, select
from app.models.powers import Powers, PowerUpdate
###################################################################################################

class PowersCrud:

###################################################################################################
# CREATE
    @staticmethod
    def create_power(
        session: Session,
        power: Powers
    ) -> Powers:
        
        """ Method to create a new power
            
            :param Session session: database session
            :param Powers power: Object Powers
        """

        # Add the power to the session and return it
        session.add(power)
        session.commit()
        session.refresh(power)

        return power
###################################################################################################


###################################################################################################
# READ
    @staticmethod
    def read_powers(
        session: Session,
        power_id: int | None = None
    ) -> list[Powers] | Powers:
        
        """ Method to return all the powers in the database or only one power
            by passing its power_id.

            :param Session session: database session
            :param int (opt) power_id: the power's ID
            :return: list of objects Powers or a object Powers
        """

        # Verify if the user give a power_id and return the result
        if power_id:
            resultado = session.exec(select(Powers)).all()
        
        else:
            resultado = session.exec(select(Powers).where(Powers.power_id == power_id)).first()

        return resultado
###################################################################################################


###################################################################################################
# UPDATE
    @staticmethod
    def update_power(
        session: Session,
        power_id: int,
        power_update: dict
    ):
        
        """ Method to update a power by passing its power_id and a PowerUpdate with
            the fields to be modified.

            :param Session session: database session
            :param int power_id: the power's ID
            :param dict power_update: a dict with the fields to be modified
            :return: the updated power
        """

        # Get the power to be updated
        power_to_update = session.get(Powers, power_id)

        # Return None if the power doesn't exist
        if not power_to_update:
            return None
        
        # Update the power
        power_to_update.sqlmodel_update(power_update)

        session.add(power_to_update)
        session.commit()
        session.refresh(power_to_update)

        # Returns the updated power
        return power_to_update
###################################################################################################


###################################################################################################
# DELETE
    @staticmethod
    def delete_power(
        session: Session,
        power_id: int
    ):
        """ Method to delete a power by passing its power_id.

            :param Session session: database session
            :param int power_id: the power's ID
            :return: the deleted power
        """

        # Get the power to be deleted
        power_to_delete = session.get(Powers, power_id)

        # Return None if the power doesn't exist
        if power_to_delete is None:
            return None
        
        # Delete the power and return it
        session.delete(power_to_delete)
        session.commit()

        return power_to_delete
###################################################################################################