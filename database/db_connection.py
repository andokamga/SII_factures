import sqlite3

DB_PATH = "application_data.db"

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")  # Activer les clés étrangères
        return conn
    except sqlite3.Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None
       
def drop_all_tables(conn):
    """
    Supprime toutes les tables existantes dans la base de données.
    """
    try:
        cursor = conn.cursor()

        # Liste des tables à supprimer
        tables = ["invoice_items", "invoices", "products", "clients", "users", "notifications", "backups"]
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
        
        conn.commit()
        print("Toutes les tables existantes ont été supprimées.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression des tables : {e}")

def initialize_database():
    conn = get_db_connection()
    if conn is None:
        print("Impossible d'initialiser la base de données.")
        return

    try:
        # Supprimer les anciennes tables
        drop_all_tables(conn)

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            total REAL NOT NULL,
            tax REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            sent_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backup_path TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        print("Base de données initialisée avec succès.")
        insert_test_data(conn)

    except sqlite3.Error as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")
    finally:
        conn.close()

def insert_test_data(conn):
    try:
        cursor = conn.cursor()

        # Utilisateurs
        users = [(f"user{i}", f"password{i}", "user" if i % 2 == 0 else "admin") for i in range(1, 16)]
        cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", users)

        # Clients
        clients = [(f"Client {i}", f"client{i}@example.com", f"12345678{i:02d}", f"Adresse {i}") for i in range(1, 16)]
        cursor.executemany("INSERT INTO clients (name, email, phone, address) VALUES (?, ?, ?, ?)", clients)

        # Produits
        products = [(f"Produit {i}", f"Description {i}", 10.0 + i * 2) for i in range(1, 16)]
        cursor.executemany("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", products)

        # Factures et articles
        invoices, invoice_items = [], []
        TAX_RATE = 0.15

        for invoice_id in range(1, 16):
            client_id = (invoice_id % 15) + 1
            total_items_price = 0

            for item_num in range(1, 4):
                product_id = (invoice_id + item_num) % 15 + 1
                quantity = item_num
                unit_price = 10.0 + product_id * 2
                item_price = unit_price * quantity

                invoice_items.append((invoice_id, product_id, quantity, item_price))
                total_items_price += item_price

            tax = total_items_price * TAX_RATE
            total_with_tax = total_items_price + tax
            invoices.append((client_id, total_with_tax, tax))

        cursor.executemany("INSERT INTO invoices (client_id, total, tax) VALUES (?, ?, ?)", invoices)
        cursor.executemany("INSERT INTO invoice_items (invoice_id, product_id, quantity, price) VALUES (?, ?, ?, ?)", invoice_items)

        # Insérer des notifications
        notifications = [
            (f"Message de notification {i}",) for i in range(1, 16)
        ]
        cursor.executemany("INSERT OR IGNORE INTO notifications (message) VALUES (?)", notifications)

        # Insérer des sauvegardes
        backups = [
            (f"backup_{i}.zip",) for i in range(1, 16)
        ]
        cursor.executemany("INSERT OR IGNORE INTO backups (backup_path) VALUES (?)", backups)

        conn.commit()
        print("Données de test insérées avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion des données : {e}")

if __name__ == "__main__":
    initialize_database()