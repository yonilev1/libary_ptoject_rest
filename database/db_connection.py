import mysql.connector

def get_connection():
    return mysql.connector.connect(
        user='root',
        password='root',
        host='127.0.0.1',
        database='library_db'
    )


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE member (
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
        CREATE TABLE book (
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
    