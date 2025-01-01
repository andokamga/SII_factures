import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        #conn.row_factory = sqlite3.Row
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

        # Création des tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
        """)
        print("Table 'users' créée.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            address TEXT
        )
        """)
        print("Table 'clients' créée.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0       
        )
        """)
        print("Table 'products' créée.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            total REAL NOT NULL,
            tax REAL NOT NULL,
            reference TEXT NOT NULL DEFAULT (REPLACE(REPLACE(REPLACE(DATETIME('now'), '-', ''), ' ', ''), ':', '')),
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE
        )
        """)
        print("Table 'invoices' créée.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        )
        """)
        print("Table 'invoice_items' créée.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            sent_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Table 'notifications' créée.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backup_path TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Table 'backups' créée.")

        conn.commit()
        print("Toutes les tables ont été créées avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création des tables : {e}")

# Fonction pour hacher un mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def insert_test_data(conn):
    try:
        cursor = conn.cursor()

        # Utilisateurs
        users = [(f"user{i}", hash_password(f"password{i}"), "user" if i % 2 == 0 else "admin") for i in range(1, 30)]
        cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", users)

        # Clients
        clients = [(f"Client {i}", f"client{i}@example.com", f"12345678{i:02d}", f"Adresse {i}") for i in range(1, 30)]
        cursor.executemany("INSERT INTO clients (name, email, phone, address) VALUES (?, ?, ?, ?)", clients)

        # Produits
        products = [(f"Produit {i}", f"Description {i}", 10.0 + i * 2, i * 2) for i in range(1, 30)]
        cursor.executemany("INSERT INTO products (name, description, price, stock_quantity) VALUES (?, ?, ?, ?)", products)

        # Factures et articles
        invoices, invoice_items = [], []
        TAX_RATE = 0.15

        for invoice_id in range(1, 30):
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
            (f"Message de notification {i}",) for i in range(1, 30)
        ]
        cursor.executemany("INSERT OR IGNORE INTO notifications (message) VALUES (?)", notifications)

        # Insérer des sauvegardes
        backups = [
            (f"backup_{i}.zip",) for i in range(1, 30)
        ]
        cursor.executemany("INSERT OR IGNORE INTO backups (backup_path) VALUES (?)", backups)

        conn.commit()
        print("Données de test insérées avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion des données : {e}")
        

if __name__ == "__main__":
    conn = get_db_connection()
    initialize_database()
    insert_test_data(conn)