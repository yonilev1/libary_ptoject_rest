from fastapi import APIRouter,status, HTTPException, Query
from database import book_db, member_db
from pydantic import BaseModel
from logs import logger

class CreateMember(BaseModel):
    name:str
    email:str

class UpdateMember(BaseModel):
    name:str | None = None
    email:str | None = None
    is_active:bool | None = None
    total_borrow:int | None = None

router = APIRouter()
my_logger = logger.get_logger('library_member_routes')

@router.post('/members', status_code=status.HTTP_201_CREATED)
def create_member(member : CreateMember):
    my_logger.info('in route create member')
    dict_member = member.model_dump()
    new_member = member_db.MemeberDb()
    try:
        new_member_id = new_member.create_member(dict_member)
        if not new_member_id:
            my_logger.error('couldnt create member')
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        my_logger.exception(f'value error accured {e}')
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    my_logger.info('finished to create member')
    

@router.get('/members')
def get_all_members():
    my_logger.info('in route get all members')
    new_member = member_db.MemeberDb()
    my_logger.info('returning all members')
    return new_member.get_all_members()


@router.get('/members/{id}')
def get_member_by_id(id:int):
    my_logger.info('in route get member by id')
    new_member = member_db.MemeberDb()
    get_member = new_member.get_member_by_id(id)
    if not get_member:
        my_logger.error(f'member {id} does not exist')
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    my_logger.info(f'returning member with id {id}')
    return get_member


@router.put('/members/{id}')
def update_member(id:int, member:UpdateMember = Query(...)):
    my_logger.info('in route update member')
    dict_member = member.model_dump(exclude_unset=True)
    new_member = member_db.MemeberDb()
    try:
        updated_member = new_member.update_member(id, dict_member)
    except Exception as e:
        my_logger.exception(f'couldnt update member {e}')
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    if updated_member == 0:
        my_logger.error(f'member is already {member}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'member is already {dict_member}')
    elif updated_member == -1:
        my_logger.error(f'member {id} does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        my_logger.info(f'finished to update member {id}')
        return 'member updated successfully'
    


@router.put('/members/{id}/deactivate')
def deactivate_member(id:int):
    my_logger.info('in route deactivate member')
    try:
        deactive = update_member(id, UpdateMember(is_active=False))
    except Exception as e:
        my_logger.exception(f'couldnt deactivate member {e}')
        raise
    my_logger.info(f'finished to deactivate member {id}')
    return 'member deactivated successfully'


@router.put('/members/{id}/activate')
def activate_member(id:int):
    my_logger.info('in route activate member')
    try:
        active = update_member(id, UpdateMember(is_active=True))
    except Exception as e:
        my_logger.exception(f'couldnt activate member {e}')
        raise
    my_logger.info(f'finished to activate member {id}')
    return 'member activated successfully'