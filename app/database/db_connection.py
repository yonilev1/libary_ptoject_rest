import mysql.connector

def get_connection():
    return mysql.connector.connect(
        user='root',
        password='root',
        host='127.0.0.1',
        database='library_db'
    )

conn = get_connection()
cur = conn.cursor()
cur.execute("SHOW DATABASES")
print("Databases:", [r[0] for r in cur.fetchall()])