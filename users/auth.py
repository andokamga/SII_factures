from database.db_connection import get_db_connection
import hashlib
import sqlite3

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Inscription d'un nouvel utilisateur
def register_user(username, password):
    conn = get_db_connection()  # Obtenir une connexion à la base de données
    hashed_password = hash_password(password)  # Hacher le mot de passe
    cursor = conn.cursor()

    try:
        # Insérer le nouvel utilisateur avec un rôle par défaut ('user')
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()  # Valider les modifications
        print(f"Utilisateur '{username}' enregistré avec succès!")
    except sqlite3.IntegrityError:
        print(f"Erreur : L'utilisateur '{username}' existe déjà.")
    finally:
        cursor.close()  # Fermer le curseur
        conn.close()  # Fermer la connexion

# Authentification d'un utilisateur
def authenticate_user(username, password):
    hashed_password = hash_password(password)  # Hacher le mot de passe saisi
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        print(f"Bienvenue, {username}!")
        print(user)
        return True
    else:
        print("Nom d'utilisateur ou mot de passe incorrect.")
        return False