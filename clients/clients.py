from database.db_connection import get_db_connection

def add_client(name, email, phone, address):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (name, email, phone, address) VALUES (?, ?, ?, ?)", (name, email, phone, address))
    conn.commit()
    conn.close()