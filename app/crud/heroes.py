# Fichero para crear el CRUD de heroes
from typing import Annotated
from sqlmodel import Session, select
from app.models.heroes import Hero


class HeroCrud():

    @staticmethod
    def create_hero(*, session: Session, hero: Hero):
        """
            Method to create new heroes

            :param Session session: database session
            :param Hero hero: Object Hero
            :return: The created Hero
        """
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


    @staticmethod
    def read_heroes(*, session: Session, hero_id: int | None = None):
        """
            Method to read heroes in database. Returns one hero if
            a hero_id is provided

            :param Session session: database session
            :param int hero_id: the hero's ID
            :return: a list of heroes or a hero
        """
        if not hero_id:
            query = select(Hero)
            result = session.exec(query).all()
        
        else:
            query = select(Hero).where(Hero.id == hero_id)
            result = session.exec(query).first()

        return result


    @staticmethod
    def update_hero(
        *, 
        session: Session, 
        hero_id: int, 
        args: dict
    ):
        '''
            Method to update an existing hero
            
            :param Session session: database session
            :param int hero_id: the hero's ID
            :param dict args: a dict with the Hero fields to be updated
            :return: the updated hero
        '''
        hero_update = session.get(Hero, hero_id)

        if not hero_update:
            return None

        if "name" in args:
            hero_update.name = args['name']
        if "secret_name" in args:
            hero_update.secret_name = args["secret_name"]
        if "age" in args:
            hero_update.age = args["age"]
        
        session.add(hero_update)
        session.commit()
        session.refresh(hero_update)

        return hero_update


    @staticmethod
    def delete_hero(
        *,
        session: Session,
        hero_id: int
    ):
        '''
            Method to delete a hero

            :param Session session: database session
            :param int hero_id: the hero's ID
            :return: the deleted hero
        '''

        hero_delete = session.get(Hero, hero_id)

        if not hero_delete:
            return None
        
        session.delete(hero_delete)
        session.commit()
        
        return hero_delete
