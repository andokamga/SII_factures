from database.db_connection import get_db_connection

def add_backup(backup_path):
    """
    Ajoute un enregistrement de sauvegarde dans la table 'backups'.
    :param backup_path: Chemin du fichier de sauvegarde.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO backups (backup_path) VALUES (?)",
            (backup_path,)
        )
        conn.commit()
        print(f"Sauvegarde ajoutée : {backup_path}")
    except Exception as e:
        print(f"Erreur lors de l'ajout de la sauvegarde : {e}")
    finally:
        conn.close()

def get_all_backups():
    """
    Récupère toutes les sauvegardes enregistrées.
    :return: Liste des sauvegardes.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM backups ORDER BY created_at DESC")
        backups = cursor.fetchall()
        print(f"{len(backups)} sauvegardes trouvées.")
        return backups
    except Exception as e:
        print(f"Erreur lors de la récupération des sauvegardes : {e}")
        return []
    finally:
        conn.close()

def get_backup_by_id(backup_id):
    """
    Récupère une sauvegarde par son ID.
    :param backup_id: ID de la sauvegarde.
    :return: Détails de la sauvegarde.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM backups WHERE id = ?", (backup_id,))
        backup = cursor.fetchone()
        if backup:
            print(f"Sauvegarde trouvée : {backup}")
        else:
            print(f"Aucune sauvegarde trouvée avec ID {backup_id}.")
        return backup
    except Exception as e:
        print(f"Erreur lors de la récupération de la sauvegarde : {e}")
        return None
    finally:
        conn.close()

def delete_backup(backup_id):
    """
    Supprime une sauvegarde par son ID.
    :param backup_id: ID de la sauvegarde à supprimer.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM backups WHERE id = ?", (backup_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Sauvegarde avec ID {backup_id} supprimée avec succès.")
        else:
            print(f"Aucune sauvegarde trouvée avec ID {backup_id}.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la sauvegarde : {e}")
    finally:
        conn.close()

def get_backups_paginated(page=1, items_per_page=10):
    """
    Récupère les sauvegardes avec pagination.
    :param page: Numéro de la page.
    :param items_per_page: Nombre d'éléments par page.
    :return: Dictionnaire contenant les sauvegardes et les informations de pagination.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        offset = (page - 1) * items_per_page

        cursor.execute("SELECT COUNT(*) FROM backups")
        total_backups = cursor.fetchone()[0]

        total_pages = (total_backups + items_per_page - 1) // items_per_page  # Arrondi vers le haut

        cursor.execute(
            "SELECT * FROM backups ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (items_per_page, offset)
        )
        backups = cursor.fetchall()

        return {
            "backups": backups,
            "total_backups": total_backups,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des sauvegardes avec pagination : {e}")
        return {
            "backups": [],
            "total_backups": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    finally:
        conn.close()

def update_backup_path(backup_id, new_path):
    """
    Met à jour le chemin d'une sauvegarde.
    :param backup_id: ID de la sauvegarde.
    :param new_path: Nouveau chemin de sauvegarde.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE backups SET backup_path = ? WHERE id = ?",
            (new_path, backup_id)
        )
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Chemin de sauvegarde mis à jour pour l'ID {backup_id}.")
        else:
            print(f"Aucune sauvegarde trouvée avec ID {backup_id}.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du chemin de sauvegarde : {e}")
    finally:
        conn.close()