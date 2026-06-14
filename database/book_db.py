from database.db_connection import get_connection

class BookDB:
    VALID_GENRE = ['Fiction',' Non-Fiction', 'Science', 'History', 'Other']
    def create_book(self, data):
        """
        create a book and store in db

        returns: number of new row or None if didnt add

        raises: valueerror if genre mot valid
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if data['genre'] not in BookDB.VALID_GENRE:
            raise ValueError(f"genre has to be from - Fiction/Non-Fiction/Science/History/Other. not {data['genre']}")
        
        cursor.execute("""
        INSERT INTO book (title, author, genre, is_available)
        VALUES(%s, %s, %s, True);
        """, (data['title'], data['author'], data['genre']))
        conn.commit()
        did_add = cursor.lastrowid
        cursor.close()
        conn.close()
        return did_add
    

    def get_all_books(self):
        """
        returns list of all books, or empty list if no books
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT * FROM book;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    

    def get_book_by_id(self, id):
        """
        returns book by id, if does not exist returns None
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT * FROM book WHERE id = %s;
        """, (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    

    def update_book(self, id, data):
        """
        update book by id, return 1 if updates else 0
        """
        if 'genre' in data.keys() and  data['genre'] not in BookDB.VALID_GENRE:
            raise ValueError(f"genre has to be from - Fiction/Non-Fiction/Science/History/Other. not {data['genre']}")
        
        in_parts = [f'{key} = %s' for key in data.keys()]
        in_str = ", ".join(in_parts)
        parsed_data =list(data.values()) + [id]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"""
        UPDATE book SET {in_str} WHERE id = %s;
        """, parsed_data)
        conn.commit()
        did_update = cursor.rowcount
        cursor.close()
        conn.close()
        return did_update
    

    def set_available(self, id, val, member_id):
        """
        update book to be avalible/unavalible
        returns 1 if succsses else 0
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"""
        SELECT is_available FROM book WHERE id = %s;
        """, (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row['is_available'] is not val:
            if row['is_available'] == 0:
                return self.update_book(id, {'is_available': val, 'borrowed_by_member_id': None})
            return self.update_book(id, {'is_available': val, 'borrowed_by_member_id': member_id})
        else:
            raise ValueError(f'cant change availability, it already {val}')
        


    def count_total_books(self):
        """
        get number of books in the db
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT COUNT(*) AS total FROM book;
        """)
        rows = cursor.fetchone()
        cursor.close()
        conn.close()
        return rows['total'] if rows else 0
    

    def count_available_books(self):
        """
        returns num of avalible books
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT COUNT(*) AS available FROM book WHERE is_available = True;
        """)
        rows = cursor.fetchone()
        cursor.close()
        conn.close()
        return rows['available'] if rows else 0
    

    def count_borrowed_books(self):
        """
        return number of borrowed books
        """
        return self.count_total_books() - self.count_available_books()
    

    def count_by_genre(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT genre as Genre, COUNT(*) as COUNT FROM book GROUP BY genre ;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    

    def count_active_borrows_by_member(self, member_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT * FROM book WHERE borrowed_by_member_id = %s ;
        """, (member_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return len(rows)
    

    def is_the_book_lent_and_to_member(self, id, member_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT  is_available, borrowed_by_member_id FROM book WHERE id = %s ;
        """,(id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row['is_available'] == False and row['borrowed_by_member_id'] == member_id:
            return True, True
        elif row['is_available'] == True and row['borrowed_by_member_id'] == None:
            return False, False
        elif row['is_available'] == False and row['borrowed_by_member_id'] != member_id:
            return True, False
    
    
    def how_meny_books_member_borrowed(self, member_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT  COUNT(*) as COUNT_BORROW FROM book WHERE borrowed_by_member_id = %s ;
        """,(member_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row['COUNT_BORROW']
