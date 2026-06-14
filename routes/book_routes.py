from fastapi import APIRouter,status, HTTPException, Query
from database import book_db, member_db
from pydantic import BaseModel

class CreateBook(BaseModel):
    title:str
    author:str
    genre:str


class UpdateBook(BaseModel):
    title:str | None = None
    author:str | None = None
    genre:str | None = None
    is_available:bool | None = None

router = APIRouter()

@router.post('/books', status_code=status.HTTP_201_CREATED)
def create_book(book : CreateBook):
    dict_book = book.model_dump()
    new_book = book_db.BookDB()
    try:
        new_book_id = new_book.create_book(dict_book)
        if not new_book_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.get('/books')
def get_all_books():
    new_book = book_db.BookDB()
    return new_book.get_all_books()


@router.get('/books/{id}')
def get_book_by_id(id:int):
    new_book = book_db.BookDB()
    get_book = new_book.get_book_by_id(id)
    if not get_book:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return get_book


@router.put('/books/{id}')
def update_book(id:int, book:UpdateBook = Query(...)):
    dict_book = book.model_dump(exclude_unset=True)
    new_book = book_db.BookDB()
    try:
        updated_book = new_book.update_book(id, dict_book)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    if updated_book == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return 'book updated successfully'
    

@router.put('/books/{id}/borrow/{member_id}')
def borrow_book(id:int, member_id:int):
    new_book = book_db.BookDB()
    new_member = member_db.MemeberDb()
    if new_member.get_member_by_id(member_id):
        if new_member.is_active_member(member_id):    
            if new_book.get_book_by_id(id):
                if new_member.count_borrowes(member_id) < 3:
                    try:
                        lend_book = new_book.set_available(id, 0, member_id)
                    except Exception as e:
                        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Book is not available')
                    if lend_book == 0:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
                    else:
                        new_member.decement_increment_borrows(member_id, 1)
                        new_member.increment_total_borrows(member_id)
                        return 'book borrowed successfully'
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Member has reached maximum borrows')
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book not found')
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Member is not active')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Member not found')
    

@router.put('/books/{id}/return/{member_id}')
def return_book(id:int, member_id:int):
    new_book = book_db.BookDB()
    new_member = member_db.MemeberDb()
    if new_member.get_member_by_id(member_id):
        if new_book.get_book_by_id(id):
            is_borrowed, to_member = new_book.is_the_book_lent_and_to_member(id, member_id)
            if is_borrowed:
                if to_member:
                    try:
                        return_book = new_book.set_available(id, 1, member_id)
                    except Exception as e:
                        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
                    if return_book == 0:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
                    else:
                        new_member.decement_increment_borrows(member_id, -1)
                        return 'book returned successfully'
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Book is not borrowed by this member')
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Book is not borrowed')
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Member not found')
                

