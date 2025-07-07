
from sqlmodel import select, Session
from app.models.villains import Villain, VillainUpdate

class VillainCrud:
    # Create
    @staticmethod
    def create_villain(
        session: Session,
        villain: Villain
    ) -> Villain:
        
        '''
            Method to create a new villain

            :param Session session: Database session
            :param Villain villain: Object Villain
            :return: The created villain
        '''
        session.add(villain)
        session.commit()
        session.refresh(villain)

        return villain


    # Read
    @staticmethod
    def read_villains(
        *,
        session: Session,
        villain_id: int | None = None
    ) -> Villain | list[Villain]:
        
        '''
            Method to return all the villains in the database or a
            villain with their respective ID.

            :param Session session: Database session
            :param int (opt) villain_id: Villain's ID
        '''

        if not villain_id:
            result = session.exec(select(Villain)).all()
        
        else:
            result = session.exec(
                select(Villain).where(Villain.id == villain_id)
            ).first()

        return result
    

    # Update
    @staticmethod
    def update_villain(
        *,
        session: Session,
        villain_id: int,
        villain: dict
    ):
        """
            Method to update a villain with their ID

            :param Session session: Database session
            :param int villain_id: Villain's ID
            :param dict villain: Dict with villain's attributes to be updated
            :return: The villain updated
        """
        # Get the villain to update
        villain_update = session.get(Villain, villain_id)

        # If not villain, return None
        if villain_update is None:
            return None
        
        # Update and return the villain
        villain_update.sqlmodel_update(villain)
        session.add(villain_update)
        session.commit()
        session.refresh(villain_update)

        return villain_update
    

    # Delete
    def delete_villain(
        *,
        session: Session,
        villain_id: int
    ):
        """
            Method to delete a villain with their ID

            :param Session session: Database session
            :param int villain_id: Villain's ID
            :return: The villain deleted
        """

        # Get the villain to delete
        villain_delete = session.get(Villain, villain_id)
        
        # If not villain, return None
        if villain_delete is None:
            return None

        # Delete and return the villain
        session.delete(villain_delete)
        session.commit()

        return villain_delete
