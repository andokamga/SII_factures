from database.db_connection import get_db_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def add_user(username, password, role="user"):
    """
    Ajoute un utilisateur dans la table 'users'.
    :param username: Le nom d'utilisateur.
    :param password: Le mot de passe de l'utilisateur.
    :param role: Le rôle de l'utilisateur, avec 'user' comme valeur par défaut.
    """
    conn = get_db_connection()
    hashed_password = hash_password(password) 
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )
        conn.commit()
        print(f"Utilisateur '{username}' ajouté avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
    finally:
        conn.close()

def get_all_users(page=1, items_per_page=10):
    """
    Récupère et retourne les utilisateurs de la table 'users' en fonction de la pagination.
    :param page: Numéro de la page à récupérer (par défaut 1).
    :param items_per_page: Nombre d'utilisateurs par page (par défaut 10).
    :return: Liste des utilisateurs pour la page demandée.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Calculer l'OFFSET (déplacement des résultats)
        offset = (page - 1) * items_per_page

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            raise Exception("La table 'users' n'existe pas.")

        # Récupérer les utilisateurs avec LIMIT et OFFSET
        cursor.execute("SELECT * FROM users LIMIT ? OFFSET ?", (items_per_page, offset))
        users = cursor.fetchall()

        if users:
            print("=== Liste des utilisateurs ===")
            for user in users:
                print(user)  # Chaque `user` est une ligne retournée par la requête
        else:
            print("Aucun utilisateur trouvé.")

        # Calculer le nombre total d'utilisateurs pour la pagination
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        total_pages = (total_users + items_per_page - 1) // items_per_page  # Arrondi vers le haut

        return {
            "users": users,
            "total_users": total_users,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }
    except Exception as e:
        print("Erreur lors de la récupération des utilisateurs : {e}")
        return {
            "users": [],
            "total_users": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    finally:
        conn.close()

def get_user_by_id(user_id):
    """
    Récupère un utilisateur spécifique par son ID.
    :param user_id: L'ID de l'utilisateur.
    :return: L'utilisateur correspondant ou None si non trouvé.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur avec ID {user_id} : {e}")
        return None
    finally:
        conn.close()

def update_user(user_id, username, password, role):
    """
    Met à jour un utilisateur existant.
    :param user_id: L'ID de l'utilisateur.
    :param username: Le nom d'utilisateur à mettre à jour.
    :param password: Le mot de passe à mettre à jour.
    :param role: Le rôle à mettre à jour.
    """
    hashed_password = hash_password(password) 
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?",
            (username, hashed_password, role, user_id)
        )
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Utilisateur avec ID {user_id} mis à jour avec succès.")
        else:
            print(f"Aucun utilisateur trouvé avec ID {user_id}.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
    finally:
        conn.close()

def delete_user(user_id):
    """
    Supprime un utilisateur spécifique par son ID.
    :param user_id: L'ID de l'utilisateur à supprimer.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Utilisateur avec ID {user_id} supprimé avec succès.")
        else:
            print(f"Aucun utilisateur trouvé avec ID {user_id}.")
    except Exception as e:
        print(f"Erreur lors de la suppression de l'utilisateur : {e}")
    finally:
        conn.close()

def filter_users_by_username(username_query, page=1, items_per_page=15):
    """
    Filtre les utilisateurs par nom d'utilisateur et applique une pagination.

    :param username_query: Chaîne de recherche à filtrer dans le nom d'utilisateur.
    :param page: Numéro de la page actuelle (par défaut 1).
    :param items_per_page: Nombre d'utilisateurs par page (par défaut 15).
    :return: Dictionnaire contenant les utilisateurs filtrés et les informations de pagination.
    """
    conn = get_db_connection()  # Assurez-vous que cette fonction retourne une connexion valide
    if not conn:
        print("Erreur : Connexion à la base de données échouée.")
        return {
            "users": [],
            "total_users": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    
    try:
        cursor = conn.cursor()

        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            raise Exception("La table 'users' n'existe pas.")

        # Préparer la recherche avec un joker pour les correspondances partielles
        query = f"%{username_query}%" if username_query.strip() else "%"

        # Compter le total des utilisateurs correspondant à la recherche
        cursor.execute("SELECT COUNT(*) FROM users WHERE username LIKE ? COLLATE NOCASE", (query,))
        total_users = cursor.fetchone()[0]

        # Calculer le nombre total de pages
        total_pages = (total_users + items_per_page - 1) // items_per_page

        # Ajuster la page si elle dépasse les limites
        if total_pages == 0:
            page = 1
        elif page > total_pages:
            page = total_pages

        # Calculer l'OFFSET pour la pagination
        offset = (page - 1) * items_per_page

        # Récupérer les utilisateurs correspondant à la recherche avec la pagination
        cursor.execute(
            "SELECT * FROM users WHERE username LIKE ? COLLATE NOCASE ORDER BY username ASC LIMIT ? OFFSET ?",
            (query, items_per_page, offset)
        )
        users = cursor.fetchall()

        # Retourner les résultats sous forme de dictionnaire
        return {
            "users": users,
            "total_users": total_users,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }

    except Exception as e:
        print(f"Erreur lors du filtrage des utilisateurs : {e}")
        return {
            "users": [],
            "total_users": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }

    finally:
        conn.close()