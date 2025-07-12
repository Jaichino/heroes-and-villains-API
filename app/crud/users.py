####################
#    User's CRUD   #
####################

###################################################################################################
# Imports
from sqlmodel import Session
from app.models.users import User, UserIn, UserOut
from app.auth.hashing import hash_password
###################################################################################################


###################################################################################################
class UserCrud:
###################################################################################################

###################################################################################################
# Create users
    @staticmethod
    def create_user(session: Session, user: UserIn) -> UserOut:

        """ Method to create new users in database. Receives an UserIn, then it hash the password
            using hash_password and finally, returns the created user without password.

            :param Session session: database session
            :param UserIn user: object with username and password
            :return: a UserOut object (user without password)
        """

        # Hash the password passed in user
        hashed_password = hash_password(user.password)

        # Create a object User (database user)
        user_db = User(username=user.username, hash_password=hashed_password)

        # Add user in database
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        
        # Return an UserOut
        return UserOut(username=user_db.username, user_id=user_db.user_id)
###################################################################################################