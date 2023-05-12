from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from ..database import engine, get_db
from .. import models, schemas, oath2
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db), current_user:int = Depends(oath2.get_current_user), limit:int=5, offset:int=0,
              search: Optional[str]=''):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    results = db.query(models.Post, func.count(models.Votes.post_id).label("vote")).join(models.Votes, models.Post.id==models.Votes.post_id, isouter=True)\
        .group_by(models.Post.id).all()
    results=list ( map (lambda x : x._mapping, results) )
    return results

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.CreatePost, db:Session=Depends(get_db), current_user:int = Depends(oath2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """, (post.title, post.content))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    post_dict = post.dict()
    post_dict.update({"owner_id":current_user.id})
    new_post = models.Post(**post_dict)
    print(new_post.owner_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db), current_user:int = Depends(oath2.get_current_user)):
    # post= find_post(id)
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id==id).first()
    post = db.query(models.Post, func.count(models.Votes.post_id).label("vote")).join(models.Votes, models.Post.id==models.Votes.post_id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"details not found for {id}")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db), current_user:int = Depends(oath2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id==id)
    
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"details not found for {id}")

    if post.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    post.delete(synchronize_session=False)
    db.commit()
    # db.refresh(post)
    return 



@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post:schemas.CreatePost, db:Session=Depends(get_db), current_user:int = Depends(oath2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s  WHERE id=%s RETURNING *""", (post.title, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    print(post_query.first())
    if not post_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"details not found for {id}")
    if post_query.first().owner_id == current_user.id:
        post_query.update(post.dict(),synchronize_session=False)
    else:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN)
    db.commit()
    return post_query.first()