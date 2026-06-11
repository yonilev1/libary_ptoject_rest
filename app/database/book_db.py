from db_connection import get_connection

class BookDB:
    VALID_GENRE = ['Fiction',' Non-Fiction', 'Science', 'History', 'Other']
    def create_book(self, title, author, genre):
        """
        create a book and store in db

        returns: number of new row or None if didnt add

        raises: valueerror if genre mot valid
        """
        conn = get_connection()
        cursor = conn.cursor()

        if genre not in BookDB.VALID_GENRE:
            raise ValueError(f"genre has to be from - Fiction/Non-Fiction/Science/History/Other. not {genre}")
        
        cursor.execute("""
        INSERT INTO book (title, author, genre, is_available)
        VALUES(%s, %s, %s, True);
        """, (title, author, genre))
        conn.commit()
        did_add = cursor.lastrowid
        cursor.close()
        conn.close()
        return did_add
    

    def get_all_books(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM book;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    

Book = BookDB()
Book.create_book('t', 't', 'Other')
print(Book.get_all_books())