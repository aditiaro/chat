from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from model import models, schemas, security
from model.database import get_db

#instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#extractin user from JWT
'''
def get_user(database: Session, username: str):
    return database.query(models.User).filter(models.User.username == username).first()
'''

async def get_current_user(
    token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:  
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username: str = payload.get("sub") #default
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username) #new token data instance
    except JWTError:
        raise credentials_exception
    '''
    user = get_user(database, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
    '''