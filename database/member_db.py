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
        INSERT INTO member (email, name, is_active, total_borrow)
        VALUES(%s, %s, True, 0);
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
        return row['total_borrow']
    

    def update_member(self, id, data):
        """
        update member by id, return 1 if updates else 0
        """
        in_parts = [f'{key} = %s' for key in data.keys()]
        in_str = ", ".join(in_parts)
        parsed_data =list(data.values()) + [id]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
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
    

    def increment_borrows(self, id):
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
        except TypeError as e:
            return row
        

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
        SELECT * FROM member ORDER BY total_borrow desc;
        """)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
        

member = MemeberDb()
"""member.create_member({'name':'Yoni', 'email':'yoli@gmail.com'})
member.vcreate_member({'name':'Yoni', 'email':'yoki@gmail.com'})"""
print(member.get_top_member())
