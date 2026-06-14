from database.db_connection import DbConnection

class DbInitializer:
    def __init__(self, db_connection: DbConnection):
        self.connection = db_connection

    def create_tables(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS member (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                email VARCHAR(255) NOT NULL UNIQUE, 
                name VARCHAR(50) NOT NULL ,
                is_active BOOLEAN NOT NULL,
                total_borrow INT NOT NULL
                ); 
            """)
        cursor.close()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                title VARCHAR(50) NOT NULL, 
                author VARCHAR(50) NOT NULL ,
                genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other') NOT NULL,
                is_available BOOLEAN NOT NULL,
                borrowed_by_member_id INT
                ); 
            """)
        cursor.close()
        conn.close()