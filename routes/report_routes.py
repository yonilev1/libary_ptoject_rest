from fastapi import APIRouter,status, HTTPException, Query
from database import book_db, member_db
from pydantic import BaseModel

router = APIRouter()

@router.get('/reports/summary')
def get_summery():
    new_book = book_db.BookDB()
    new_member = member_db.MemeberDb()
    total_books = new_book.count_total_books()
    available_books = new_book.count_available_books()
    active_members = new_member.count_active_members()
    return {"total_books": total_books, "available_books": available_books, "currently_borrowed": total_books - available_books, "active_members": active_members}


@router.get('/reports/books-by-genre')
def get_books_by_genre():
    new_book = book_db.BookDB()
    return new_book.count_by_genre()


@router.get('/reports/top-member')
def get_top_member():
    new_member = member_db.MemeberDb()
    return new_member.get_top_member()