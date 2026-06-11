from db_connection import get_connection

class BookDB:
    VALID_GENRE = ['Fiction',' Non-Fiction', 'Science', 'History', 'Other']
    def create_book(self, title, author, genre):
        conn = get_connection()
        cursor = conn.cursor()

        if genre not in BookDB.VALID_GENRE:
            raise ValueError(f"genre has to be from - Fiction/Non-Fiction/Science/History/Other. not {genre}")
        
        cursor.execute("""
        INSERT INTO book (title, author, genre, is_available)
        VALUES(%s, %s, %s, True);
        """(title, author, genre))
        did_add = cursor.lastrowid
        cursor.close()
        conn.close()
        return did_add