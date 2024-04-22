from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schema, oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix = "/posts",
                   tags = ["Posts"]
                   )

#Retrieve all posts
@router.get("/", response_model = List[schema.PostVote])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional["str"] = " "):
    # cursor.execute(""" SELECT * FROM app""")
    # posts = cursor.fetchall()

    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id, 
                                isouter = True).groupby(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #.....ERROR SOLVED CHECK AGAIN.....#
    results = list(map(lambda x : x._mapping, results))
    
    return results

#Create a post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    # Set the owner_id to current_user id from token
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())         # {**posts.model_dump() unpacks the dictionary form of posts and intializes values simultaneously}
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 

    return new_post

#Retrieve a single post
@router.get("/{id}", response_model = schema.PostVote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post = find_post(id)
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id,
                                                    isouter = True).groupby(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} is not found") 
    
    return post
 
 #Deleting a post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # index= find_index(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} not found")
    #Authorization so that only the owner deletes their post
    if post.id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorised to do this operation.")
    
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
    
#Updating a post
@router.put("/{id}", response_model = schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # index= find_index(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} not found")
    if post.id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorised to this operation.")
    
    post_query.update(updated_post.model_dump(), synchronize_session = False)
    db.commit()
    return post

