from database.db_connection import get_connection

class MemeberDb:
    def create_member(self, data):
        """
        create a member and store in db

        returns: number of new row or None if didnt add

        raises: valueerror if genre mot valid
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if self.email_exists(data['email']):
            raise ValueError('email already exists')

        cursor.execute("""
        INSERT INTO member (email, name, is_active, borrowed_now, total_borrow)
        VALUES(%s, %s, True, 0, 0);
        """, (data['email'], data['name']))
        conn.commit()
        did_add = cursor.lastrowid
        cursor.close()
        conn.close()
        return did_add
    

    def email_exists(self, email):
        """
        check if email exist
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT email FROM member WHERE email = %s;
        """, (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return True if row is not None else False
    

    def member_exists(self, id):
        """
        check if user exist
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT * FROM member WHERE id = %s;
        """, (id,))
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        return True if len(row) > 0 else False
    

    def get_all_members(self):
        """
        returns list of all members, or empty list if no members
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT * FROM member;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    

    def get_member_by_id(self,id):
        """
        returns member by id, if does not exist returns None
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT * FROM member WHERE id = %s;
        """, (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    
    def count_borrowes(self, id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT total_borrow FROM member WHERE id = %s;
        """, (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row is not None:
            return row['total_borrow']
        raise KeyError('id does not exist')
    

    def count_borrowes_active_now(self, id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT borrowed_now FROM member WHERE id = %s;
        """, (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row is not None:
            return row['borrowed_now']
        raise KeyError('id does not exist')
    

    def update_member(self, id, data):
        """
        update member by id, return 1 if updates else 0
        """
        in_parts = [f'{key} = %s' for key in data.keys()]
        in_str = ", ".join(in_parts)
        parsed_data =list(data.values()) + [id]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT COUNT(*) FROM member WHERE id = %s
        """,(id,))
        row = cursor.fetchone()['COUNT(*)']
        if row is 0:
            return -1
        
        cursor.close()
        cursor = conn.cursor()
        cursor.execute(f"""
        UPDATE member SET {in_str} WHERE id = %s;
        """, parsed_data)
        conn.commit()
        did_update = cursor.rowcount
        cursor.close()
        conn.close()
        return did_update
    

    def deactivate_member(self, id):
        """
        deactivates member, returns 1 if success else 0
        """
        return self.update_member(id, {'is_active': False})
    

    def activate_member(self, id):
        """
        activates member, returns 1 if success else 0
        """
        return self.update_member(id, {'is_active': True})
    

    def is_active_member(self, id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT is_active FROM member WHERE id = %s;
        """, (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row['is_active']
    

    def decement_increment_borrows(self, id, up_or_down):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT borrowed_now FROM member WHERE id = %s;
        """, (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        try:
            return self.update_member(id, {'borrowed_now': row['borrowed_now'] + up_or_down})
        except TypeError:
            return row
        

    def increment_total_borrows(self, id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT total_borrow FROM member WHERE id = %s;
        """, (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        try:
            return self.update_member(id, {'total_borrow': row['total_borrow'] + 1})
        except TypeError:
            raise KeyError('Member Not Found')
        

    def count_active_members(self):
        """
        returns num of active members
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT COUNT(*) AS active FROM member WHERE is_active = True;
        """)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row['active'] if row else row
    

    def get_top_member(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
        SELECT id as member_id, total_borrow as borrowed FROM member ORDER BY total_borrow desc;
        """)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
        

member = MemeberDb()
"""member.create_member({'name':'Yoni', 'email':'yoli@gmail.com'})
member.vcreate_member({'name':'Yoni', 'email':'yoki@gmail.com'})"""
print(member.get_top_member())
