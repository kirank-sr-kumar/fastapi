from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from .. import models, schemas, utils
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/user',
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.User)
def create_user(user:schemas.CreateUser, db:Session=Depends(get_db)):
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.User)
def get_user(id:int, db: Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    return user