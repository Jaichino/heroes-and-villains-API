# Fichero para crear el CRUD de heroes
from typing import Annotated
from sqlmodel import Session, select
from app.models.heroes import Hero


class HeroCrud():

    @staticmethod
    def create_hero(*, session: Session, hero: Hero):
        '''
            Método para la creación de un nuevo heroe
        '''
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


    @staticmethod
    def read_heroes(*, session: Session, hero_id: int | None = None):
        '''
            Método para devolver heroes de la base de datos. Si se pasa
            un hero_id, se devuelve únicamente el heroe con dicho id
        '''
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
            Método para la actualización de un heroe con determinado hero_id
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
            Método para eliminar un determinado heroe con su
            hero_id
        '''

        hero_delete = session.get(Hero, hero_id)

        if not hero_delete:
            return None
        
        session.delete(hero_delete)
        session.commit()
        
        return hero_delete
