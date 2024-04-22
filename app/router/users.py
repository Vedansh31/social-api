from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schema, utils
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/users",
                   tags = ["Users"]
                   )

#Create a user
@router.post("/", status_code = status.HTTP_201_CREATED , response_model = schema.User)
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):

    #Hashing the password
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model = schema.User)
def get_user(id: int, db: Session = Depends(get_db)):
    req_user = db.query(models.User).filter(models.User.id == id).first()

    if not req_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} not found.")
    
    return req_user

