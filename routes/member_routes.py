from fastapi import APIRouter,status, HTTPException, Query
from database import member_db, member_db
from pydantic import BaseModel

class CreateMember(BaseModel):
    name:str
    email:str

class UpdateMember(BaseModel):
    name:str | None = None
    email:str | None = None
    is_active:str | None = None
    total_borrow:int | None = None

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
    

@router.get('/members')
def get_all_members():
    new_member = member_db.MemeberDb()
    return new_member.get_all_members()


@router.get('/members/{id}')
def get_member_by_id(id:int):
    new_member = member_db.MemeberDb()
    get_member = new_member.get_member_by_id(id)
    if not get_member:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return get_member


@router.put('/members/{id}')
def update_member(id:int, member:UpdateMember = Query(...)):
    dict_member = member.model_dump(exclude_unset=True)
    new_member = member_db.MemeberDb()
    try:
        updated_member = new_member.update_member(id, dict_member)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    if updated_member == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return 'member updated successfully'
