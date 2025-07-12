#############################
#    API Router for login   #
#############################

###################################################################################################
# Imports
from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.auth.hashing import verify_password
from app.auth.auth import get_access_token, TOKEN_EXPIRE_MINUTES
from app.db.database import get_session
from app.models.users import User, UserIn, UserOut
from app.crud.users import UserCrud
####################################################################################################


###################################################################################################
# Router configuration
router = APIRouter(
    prefix="/login",
    tags=["Login"]
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
# Endpoint to login users
@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Login to access",
    responses={
        status.HTTP_200_OK:{
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "thesecretjwttoken",
                        "token_type": "bearer"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect username or password"
                    }
                }
            }
        }
    }
)
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> JSONResponse:
    
    # Get the hashed_password using form_date.username
    hashed_password = UserCrud.get_hashed_password(
        session=session,
        username=form_data.username
    )

    # Raise exception if the hashed_password is None (incorrect username)
    if hashed_password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verify the password passed with the hashed_password
    user = verify_password(
        plain_password=form_data.password,
        hashed_password=hashed_password
    )

    # Raise exception if the password is incorrect
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Create the access token
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    
    access_token = get_access_token(
        data={"sub": form_data.username},
        expiration=access_token_expires
    )

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type":"bearer"
        }
    )

    return response
