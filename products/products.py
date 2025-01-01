from database.db_connection import get_db_connection

# Ajouter un produit
def add_product(name, description, price,stock):
    """
    Ajoute un nouveau produit dans la table 'products'.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, price, stock_quantity) VALUES (?, ?, ?, ?)",
            (name, description, price, stock)
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

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        if not cursor.fetchone():
            raise Exception("La table 'products' n'existe pas.")

        # Récupérer les produits avec LIMIT et OFFSET
        cursor.execute("SELECT * FROM products LIMIT ? OFFSET ?", (items_per_page, offset))
        products = cursor.fetchall()

        if products:
            print("=== Liste des produits ===")
            for product in products:
                print(product)  # Chaque `product` est une ligne retournée par la requête
        else:
            print("Aucun produit trouvé.")

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
        print("Erreur lors de la récupération des produits : {e}")
        return {
            "products": [],
            "total_products": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    finally:
        conn.close()

def filter_products_by_name(name_query, page=1, items_per_page=15):
    """
    Filtre les produits par nom et applique une pagination.

    :param name_query: Chaîne de recherche à filtrer dans le nom des produits.
    :param page: Numéro de la page actuelle (par défaut 1).
    :param items_per_page: Nombre de produits par page (par défaut 15).
    :return: Dictionnaire contenant les produits filtrés et les informations de pagination.
    """
    conn = get_db_connection()  # Assurez-vous que cette fonction retourne une connexion valide
    if not conn:
        print("Erreur : Connexion à la base de données échouée.")
        return {
            "products": [],
            "total_products": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    try:
        cursor = conn.cursor()

        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        if not cursor.fetchone():
            raise Exception("La table 'products' n'existe pas.")

        # Préparer la recherche avec un joker pour les correspondances partielles
        query = f"%{name_query}%" if name_query.strip() else "%"
        print(f"Requête filtrée : {query}")  # Debug

        # Compter le total des produits correspondant à la recherche
        cursor.execute("SELECT COUNT(*) FROM products WHERE name LIKE ? COLLATE NOCASE", (query,))
        total_products = cursor.fetchone()[0]
        print(f"Produits totaux trouvés : {total_products}")  # Debug

        # Calculer le nombre total de pages
        total_pages = (total_products + items_per_page - 1) // items_per_page

        # Ajuster la page si elle dépasse les limites
        if total_pages == 0:
            page = 1
        elif page > total_pages:
            page = total_pages

        # Calculer l'OFFSET pour la pagination
        offset = (page - 1) * items_per_page
        print(f"OFFSET : {offset}, LIMIT : {items_per_page}")  # Debug

        # Récupérer les produits correspondant à la recherche avec la pagination
        cursor.execute(
            "SELECT * FROM products WHERE name LIKE ? COLLATE NOCASE ORDER BY name ASC LIMIT ? OFFSET ?",
            (query, items_per_page, offset)
        )
        products = cursor.fetchall()
        if products:
            print("=== Liste des produits ===")
            for product in products:
                print(product)  # Chaque `product` est une ligne retournée par la requête
        else:
            print("Aucun produit trouvé.")

        # Retourner les résultats sous forme de dictionnaire
        return {
            "products": products,
            "total_products": total_products,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }

    except Exception as e:
        print(f"Erreur lors du filtrage des produits : {e}")
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
def update_product(product_id, name, description, price,stock):
    """
    Met à jour un produit existant.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET name = ?, description = ?, price = ? , stock_quantity = ?WHERE id = ?",
            (name, description, price, stock, product_id)
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

