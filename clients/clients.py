from database.db_connection import get_db_connection

def add_client(name, email, phone, address):
    """
    Ajoute un nouveau client dans la table 'clients'.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (name, email, phone, address) VALUES (?, ?, ?, ?)",
            (name, email, phone, address)
        )
        conn.commit()
        print(f"Client '{name}' ajouté avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du client : {e}")
    finally:
        conn.close()

def get_all_clients(page=1, items_per_page=10):
    """
    Récupère et retourne les clients de la table 'clients' en fonction de la pagination.

    :param page: Numéro de la page à récupérer (par défaut 1).
    :param items_per_page: Nombre de clients par page (par défaut 10).
    :return: Liste des clients pour la page demandée.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Calculer l'OFFSET (déplacement des résultats)
        offset = (page - 1) * items_per_page

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
        if not cursor.fetchone():
            raise Exception("La table 'clients' n'existe pas.")

        # Récupérer les clients avec LIMIT et OFFSET
        cursor.execute("SELECT * FROM clients LIMIT ? OFFSET ?", (items_per_page, offset))
        clients = cursor.fetchall()

        if clients:
            print("=== Liste des clients ===")
            for client in clients:
                print(client)  # Chaque `client` est une ligne retournée par la requête
        else:
            print("Aucun client trouvé.")

        # Calculer le nombre total de clients pour la pagination
        cursor.execute("SELECT COUNT(*) FROM clients")
        total_clients = cursor.fetchone()[0]
        total_pages = (total_clients + items_per_page - 1) // items_per_page  # Arrondi vers le haut

        return {
            "clients": clients,
            "total_clients": total_clients,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des clients : {e}")
        return {
            "clients": [],
            "total_clients": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    finally:
        conn.close()

def get_client_by_id(client_id):
    """
    Récupère un client spécifique par son ID.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        client = cursor.fetchone()
        return client
    except Exception as e:
        print(f"Erreur lors de la récupération du client avec ID {client_id} : {e}")
        return None
    finally:
        conn.close()

def update_client(client_id, name, email, phone, address):
    """
    Met à jour un client existant.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clients SET name = ?, email = ?, phone = ?, address = ? WHERE id = ?",
            (name, email, phone, address, client_id)
        )
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Client avec ID {client_id} mis à jour avec succès.")
        else:
            print(f"Aucun client trouvé avec ID {client_id}.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du client : {e}")
    finally:
        conn.close()

def delete_client(client_id):
    """
    Supprime un client spécifique par son ID.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Client avec ID {client_id} supprimé avec succès.")
        else:
            print(f"Aucun client trouvé avec ID {client_id}.")
    except Exception as e:
        print(f"Erreur lors de la suppression du client : {e}")
    finally:
        conn.close()

def filter_clients_by_phone(phone_query, page=1, items_per_page=15):
    """
    Filtre les clients par numéro de téléphone et applique une pagination.

    :param phone_query: Chaîne de recherche à filtrer dans le numéro de téléphone des clients.
    :param page: Numéro de la page actuelle (par défaut 1).
    :param items_per_page: Nombre de clients par page (par défaut 15).
    :return: Dictionnaire contenant les clients filtrés et les informations de pagination.
    """
    conn = get_db_connection()  # Assurez-vous que cette fonction retourne une connexion valide
    if not conn:
        print("Erreur : Connexion à la base de données échouée.")
        return {
            "clients": [],
            "total_clients": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    try:
        cursor = conn.cursor()

        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
        if not cursor.fetchone():
            raise Exception("La table 'clients' n'existe pas.")

        # Préparer la recherche avec un joker pour les correspondances partielles
        query = f"%{phone_query}%" if phone_query.strip() else "%"
        print(f"Requête filtrée : {query}")  # Debug

        # Compter le total des clients correspondant à la recherche
        cursor.execute("SELECT COUNT(*) FROM clients WHERE phone LIKE ? COLLATE NOCASE", (query,))
        total_clients = cursor.fetchone()[0]
        print(f"Clients totaux trouvés : {total_clients}")  # Debug

        # Calculer le nombre total de pages
        total_pages = (total_clients + items_per_page - 1) // items_per_page

        # Ajuster la page si elle dépasse les limites
        if total_pages == 0:
            page = 1
        elif page > total_pages:
            page = total_pages

        # Calculer l'OFFSET pour la pagination
        offset = (page - 1) * items_per_page
        print(f"OFFSET : {offset}, LIMIT : {items_per_page}")  # Debug

        # Récupérer les clients correspondant à la recherche avec la pagination
        cursor.execute(
            "SELECT * FROM clients WHERE phone LIKE ? COLLATE NOCASE ORDER BY phone ASC LIMIT ? OFFSET ?",
            (query, items_per_page, offset)
        )
        clients = cursor.fetchall()
        if clients:
            print("=== Liste des clients ===")
            for client in clients:
                print(client)  # Chaque `client` est une ligne retournée par la requête
        else:
            print("Aucun client trouvé.")

        # Retourner les résultats sous forme de dictionnaire
        return {
            "clients": clients,
            "total_clients": total_clients,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }

    except Exception as e:
        print(f"Erreur lors du filtrage des clients : {e}")
        return {
            "clients": [],
            "total_clients": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }

    finally:
        conn.close()

def filter_clients_by_id(id_query, page=1, items_per_page=15):
    """
    Filtre les clients par ID et applique une pagination.

    :param id_query: ID du client à rechercher.
    :param page: Numéro de la page actuelle (par défaut 1).
    :param items_per_page: Nombre de clients par page (par défaut 15).
    :return: Dictionnaire contenant les clients filtrés et les informations de pagination.
    """
    conn = get_db_connection()  # Assurez-vous que cette fonction retourne une connexion valide
    if not conn:
        print("Erreur : Connexion à la base de données échouée.")
        return {
            "clients": [],
            "total_clients": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }

    try:
        cursor = conn.cursor()

        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
        if not cursor.fetchone():
            raise Exception("La table 'clients' n'existe pas.")

        # Recherche exacte par ID
        query = id_query  # L'ID est une valeur unique, donc pas besoin de LIKE
        print(f"Requête filtrée : {query}")  # Debug

        # Compter le total des clients correspondant à la recherche
        cursor.execute("SELECT COUNT(*) FROM clients WHERE id = ?", (query,))
        total_clients = cursor.fetchone()[0]
        print(f"Clients totaux trouvés : {total_clients}")  # Debug

        # Calculer le nombre total de pages
        total_pages = (total_clients + items_per_page - 1) // items_per_page

        # Ajuster la page si elle dépasse les limites
        if total_pages == 0:
            page = 1
        elif page > total_pages:
            page = total_pages

        # Calculer l'OFFSET pour la pagination
        offset = (page - 1) * items_per_page
        print(f"OFFSET : {offset}, LIMIT : {items_per_page}")  # Debug

        # Récupérer les clients correspondant à la recherche avec la pagination
        cursor.execute(
            "SELECT * FROM clients WHERE id = ? ORDER BY id ASC LIMIT ? OFFSET ?",
            (query, items_per_page, offset)
        )
        clients = cursor.fetchall()
        
        if clients:
            print("=== Liste des clients ===")
            for client in clients:
                print(client)  # Chaque client est une ligne retournée par la requête
        else:
            print("Aucun client trouvé.")

        # Retourner les résultats sous forme de dictionnaire
        return {
            "clients": clients,
            "total_clients": total_clients,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }

    finally:
        conn.close()