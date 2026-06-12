from db_connection import get_connection

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



member = MemeberDb()
"""member.create_member({'name':'Yoni', 'email':'yoli@gmail.com'})
member.create_member({'name':'Yoni', 'email':'yoki@gmail.com'})"""
print(member.get_member_by_id(54))
