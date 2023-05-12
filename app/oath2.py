from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from.config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expiry_time


def create_token(data:dict):
    to_encode = data.copy()
    expiry = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expiry})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str, credential_excep):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload["user_id"]
        if id is None:
            raise credential_excep
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_excep
    
    return token_data

def get_current_user(token: str=Depends(oauth2_schema), db:Session = Depends(database.get_db) ):
    credential_excep = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate':'Bearer'})
    token = verify_token(token, credential_excep)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user
