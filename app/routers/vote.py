from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from .. import database, models, schemas, oath2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def voting(vote:schemas.Vote,db: Session=Depends(database.get_db), current_user:int = Depends(oath2.get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id==vote.post_id, models.Votes.user_id==current_user.id)
    found_vote = vote_query.first()

    if vote.direc==1:
        if found_vote:
             raise HTTPException(
                  status_code=status.HTTP_409_CONFLICT, detail="already voted"
             )
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return "voted"
    else:
        if found_vote:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return "deleted"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)