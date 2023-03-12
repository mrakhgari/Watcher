from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_api.schemas import UserDisplay, UserBase
from database_api.db.database import get_db
from database_api.db import db_user

router = APIRouter(prefix='/users', tags=['user'])


@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db:Session = Depends(get_db)):
    return db_user.create_user(request, db)