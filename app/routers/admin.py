#############################
#    API Router for Admin   #
#############################


###################################################################################################
# Imports
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session
from app.db.database import get_session
from app.models.users import User, UserIn, UserOut
from app.crud.users import UserCrud
####################################################################################################


###################################################################################################
# Router configuration
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)
###################################################################################################


###################################################################################################
# Session dependency
SessionDep = Annotated[Session, Depends(get_session)]
###################################################################################################


###################################################################################################
# Endpoints
###################################################################################################

###################################################################################################
# Endpoint to create a user
@router.post(
    "/",
    response_model=UserOut,
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Created",
            "content": {
                "application/json": {
                    "example": {
                        "username": "juani",
                        "user_id": 1
                    }
                }
            }
        }
    }
)
async def create_user(
    session: SessionDep,
    user: Annotated[UserIn, Body(example={
        "username": "juani",
        "password": "secretpassword"
    })]
) -> UserOut:
    
    """ Function to create a new user by passing a body with the following
        fields:

        - **username**: a string username
        - **password**: a string password
    """

    # Create the user
    new_user = UserCrud.create_user(session=session, user=user)

    # Raise Exception if the username already exists
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The username already exists!"
        )

    # Return the user
    return new_user
###################################################################################################

###################################################################################################
###################################################################################################