from fastapi import APIRouter,status, HTTPException, Query
from database import book_db
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
