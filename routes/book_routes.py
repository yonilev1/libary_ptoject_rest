from fastapi import APIRouter,status, HTTPException, Query
from database import book_db, member_db
from pydantic import BaseModel
from logs import logger

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
my_logger = logger.get_logger('library_book_routes')

@router.post('/books', status_code=status.HTTP_201_CREATED)
def create_book(book : CreateBook):
    my_logger.info('in route create book')
    dict_book = book.model_dump()
    new_book = book_db.BookDB()
    try:
        new_book_id = new_book.create_book(dict_book)
        if not new_book_id:
            my_logger.error('couldnt create book')
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        my_logger.exception(f'value error accured {e}')
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    my_logger.info('finished to create book')
    

@router.get('/books')
def get_all_books():
    my_logger.info('in route get all books')
    new_book = book_db.BookDB()
    my_logger.info('returning all books')
    return new_book.get_all_books()


@router.get('/books/{id}')
def get_book_by_id(id:int):
    my_logger.info('in route get book by id')
    new_book = book_db.BookDB()
    get_book = new_book.get_book_by_id(id)
    if not get_book:
        my_logger.error(f'book {id} does not exist')
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    my_logger.info(f'returning book with id {id}')
    return get_book


@router.put('/books/{id}')
def update_book(id:int, book:UpdateBook = Query(...)):
    my_logger.info('in route update book')
    dict_book = book.model_dump(exclude_unset=True)
    new_book = book_db.BookDB()
    try:
        updated_book = new_book.update_book(id, dict_book)
    except Exception as e:
        my_logger.exception(f'couldnt create book {e}')
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    if updated_book == 0:
        my_logger.error(f'member is already {book}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'member is already {dict_book}')
    if updated_book == -1:
        my_logger.error(f'book {id} does not exist')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        my_logger.info(f'finished to update book {id}')
        return 'book updated successfully'
    

@router.put('/books/{id}/borrow/{member_id}')
def borrow_book(id:int, member_id:int):
    my_logger.info('in route borrow book')
    new_book = book_db.BookDB()
    new_member = member_db.MemeberDb()
    if new_member.get_member_by_id(member_id):
        if new_member.is_active_member(member_id):    
            if new_book.get_book_by_id(id):
                if new_book.how_meny_books_member_borrowed(member_id) < 3:
                    try:
                        lend_book = new_book.set_available(id, 0, member_id)
                    except Exception as e:
                        my_logger.exception(f'couldnt lend book {e}')
                        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Book is not available')
                    if lend_book == 0:
                        my_logger.error(f'could not lend book {id}')
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
                    else:
                        new_member.increment_total_borrows(member_id)
                        my_logger.info(f'book {id} borrowed successfully by member {member_id}')
                        return 'book borrowed successfully'
                else:
                    my_logger.error(f'Member {member_id} has reached maximum borrows')
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Member has reached maximum borrows')
            else:
                my_logger.error(f'Book not found')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book not found')
        else:
            my_logger.error(f'Member is not active')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Member is not active')
    else:
        my_logger.error(f'Member not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Member not found')
    

@router.put('/books/{id}/return/{member_id}')
def return_book(id:int, member_id:int):
    my_logger.info('in route return book')
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
                        my_logger.exception(f'couldnt return book {e}')
                        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
                    if return_book == 0:
                        my_logger.error(f'couldnt return book')
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
                    else:
                        my_logger.info(f'book {id} returned successfully by member {member_id}')
                        return 'book returned successfully'
                else:
                    my_logger.error(f'Book is not borrowed by this member')
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Book is not borrowed by this member')
            else:
                my_logger.error(f'Book is not borrowed')
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Book is not borrowed')
        else:
            my_logger.error(f'Book not found')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book not found')
    else:
        my_logger.error(f'Member not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Member not found')
                

