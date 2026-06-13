from fastapi import APIRouter,status, HTTPException, Query
from database import book_db, member_db
from pydantic import BaseModel

class CreateMember(BaseModel):
    name:str
    email:str

class UpdateMember(BaseModel):
    name:str | None = None
    email:str | None = None
    is_active:str | None = None
    total_borrow:bool | None = None

router = APIRouter()

@router.post('/members', status_code=status.HTTP_201_CREATED)
def create_member(member : CreateMember):
    dict_member = member.model_dump()
    new_member = member_db.MemeberDb()
    try:
        new_member_id = new_member.create_member(dict_member)
        if not new_member_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))