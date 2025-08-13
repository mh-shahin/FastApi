from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..hashing import Hash

router = APIRouter(
    tags=["Authentication"]
)

get_db = database.get_db

@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first(   )
    if not user:
        raise HTTPException(status_code=404, detail=f"User not Credential")
    
    if not Hash.veryfy(user.password, request.password):
        raise HTTPException(status_code=404, detail=f"Incorrect password")
    return user