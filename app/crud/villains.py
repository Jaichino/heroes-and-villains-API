
from sqlmodel import select, Session
from app.models.villains import Villain

class VillainCrud:

    @staticmethod
    def create_villain(
        session: Session,
        villain: Villain
    ):
        session.add(villain)
        session.commit()
        session.refresh(villain)

        return villain