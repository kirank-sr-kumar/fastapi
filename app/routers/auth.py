from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..import database, schemas, models,utils, oath2


router=APIRouter(tags=["Authentication"])

@router.get('/login', response_model= schemas.Token)
def login_user(user_cred:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):

    # OAuth2PasswordRequestForm contains only "username" abd "password" fields so change it from email to username
    user = db.query(models.Users).filter(models.Users.email==user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oath2.create_token(data={"user_id":user.id})
    return{"access_token":access_token, 'token_type':"bearer"}