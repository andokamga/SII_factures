from database.db_connection import get_db_connection

# Ajouter un produit
def add_product(name, description, price):
    """
    Ajoute un nouveau produit dans la table 'products'.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
            (name, description, price)
        )
        conn.commit()
        print(f"Produit '{name}' ajouté avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du produit : {e}")
    finally:
        conn.close()

def get_all_products(page=1, items_per_page=10):
    """
    Récupère et retourne les produits de la table 'products' en fonction de la pagination.

    :param page: Numéro de la page à récupérer (par défaut 1).
    :param items_per_page: Nombre de produits par page (par défaut 10).
    :return: Liste des produits pour la page demandée.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Calculer l'OFFSET (déplacement des résultats)
        offset = (page - 1) * items_per_page

        # Récupérer les produits avec LIMIT et OFFSET
        cursor.execute("SELECT * FROM products LIMIT ? OFFSET ?", (items_per_page, offset))
        products = cursor.fetchall()

        # Calculer le nombre total de produits pour la pagination
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        total_pages = (total_products + items_per_page - 1) // items_per_page  # Arrondi vers le haut

        return {
            "products": products,
            "total_products": total_products,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
        return {
            "products": [],
            "total_products": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    finally:
        conn.close()

# Récupérer un produit par son ID
def get_product_by_id(product_id):
    """
    Récupère un produit spécifique par son ID.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        return product
    except Exception as e:
        print(f"Erreur lors de la récupération du produit avec ID {product_id} : {e}")
        return None
    finally:
        conn.close()

# Mettre à jour un produit
def update_product(product_id, name, description, price):
    """
    Met à jour un produit existant.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?",
            (name, description, price, product_id)
        )
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Produit avec ID {product_id} mis à jour avec succès.")
        else:
            print(f"Aucun produit trouvé avec ID {product_id}.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du produit : {e}")
    finally:
        conn.close()

# Supprimer un produit
def delete_product(product_id):
    """
    Supprime un produit spécifique par son ID.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Produit avec ID {product_id} supprimé avec succès.")
        else:
            print(f"Aucun produit trouvé avec ID {product_id}.")
    except Exception as e:
        print(f"Erreur lors de la suppression du produit : {e}")
    finally:
        conn.close()