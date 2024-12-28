from database.db_connection import get_db_connection

def create_invoice(client_id, total, tax):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO invoices (client_id, total, tax) VALUES (?, ?, ?)", (client_id, total, tax))
    conn.commit()
    conn.close()