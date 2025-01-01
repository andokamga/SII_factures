from database.db_connection import get_db_connection

def create_invoice(client_id, total, tax):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO invoices (client_id, total, tax) VALUES (?, ?, ?)",
            (client_id, total, tax)
        )
        conn.commit()
        
        # Récupérer l'ID de la facture nouvellement insérée
        invoice_id = cursor.lastrowid  # L'ID de la facture générée automatiquement
        
        # Créer l'objet de la facture
        invoice = {
            "id": invoice_id,
            "client_id": client_id,
            "total": total,
            "tax": tax,
        }
        
        print(f"Facture pour le client ID {client_id} créée avec succès. ID: {invoice_id}")
        return invoice  # Retourner l'objet de la facture

    except Exception as e:
        print(f"Erreur lors de la création de la facture : {e}")
        return None  # Retourner None en cas d'erreur

    finally:
        conn.close()

def add_item_to_invoice(invoice_id, product_id, quantity, price):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO invoice_items (invoice_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            (invoice_id, product_id, quantity, price)
        )
        conn.commit()
        print(f"Produit ID {product_id} ajouté à la facture ID {invoice_id} avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du produit à la facture : {e}")
    finally:
        conn.close()

def get_invoice_with_items(invoice_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Récupérer les informations de la facture
        cursor.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
        invoice = cursor.fetchone()
        
        if invoice:
            print(f"Facture ID {invoice_id}: {invoice}")
            # Récupérer les éléments de la facture
            cursor.execute("SELECT * FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
            items = cursor.fetchall()
            
            if items:
                print("Éléments de la facture :")
                for item in items:
                    print(item)  # Afficher chaque élément de la facture
            else:
                print("Aucun article trouvé pour cette facture.")
        else:
            print(f"Facture ID {invoice_id} non trouvée.")
        
        return invoice, items
    except Exception as e:
        print(f"Erreur lors de la récupération de la facture et de ses éléments : {e}")
    finally:
        conn.close()

def update_invoice(invoice_id, total, tax):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE invoices SET total = ?, tax = ? WHERE id = ?",
            (total, tax, invoice_id)
        )
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Facture ID {invoice_id} mise à jour avec succès.")
        else:
            print(f"Aucune facture trouvée avec ID {invoice_id}.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la facture : {e}")
    finally:
        conn.close()

def delete_invoice(invoice_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Supprimer les éléments de la facture d'abord
        cursor.execute("DELETE FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
        
        # Puis supprimer la facture
        cursor.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Facture ID {invoice_id} supprimée avec succès.")
        else:
            print(f"Aucune facture trouvée avec ID {invoice_id}.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la facture : {e}")
    finally:
        conn.close()


def get_all_invoices(page=1, items_per_page=10):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Calculer l'OFFSET (déplacement des résultats)
        offset = (page - 1) * items_per_page
        
        cursor.execute("SELECT * FROM invoices LIMIT ? OFFSET ?", (items_per_page, offset))
        invoices = cursor.fetchall()
        
        if invoices:
            print("=== Liste des factures ===")
            for invoice in invoices:
                print(invoice)
        else:
            print("Aucune facture trouvée.")
        cursor.execute("SELECT COUNT(*) FROM invoices")
        total_invoices = cursor.fetchone()[0]
        total_pages = (total_invoices + items_per_page - 1) // items_per_page  

        return {
            "invoices": invoices,
            "total_invoices": total_invoices,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des factures : {e}")
        return {
            "invoices": [],
            "total_invoices": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    finally:
        conn.close()

def get_invoices_by_phone(phone, page=1, items_per_page=10):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clients WHERE phone = ?", (phone,))
        client = cursor.fetchone()

        if not client:
            print(f"Aucun client trouvé avec le numéro de téléphone {phone}.")
            return {
                "invoices": [],
                "total_invoices": 0,
                "total_pages": 0,
                "current_page": page,
                "items_per_page": items_per_page
            }

        client_id = client[0]
        print(f"Client ID trouvé : {client_id}")
        offset = (page - 1) * items_per_page
        cursor.execute(
            "SELECT * FROM invoices WHERE client_id = ? LIMIT ? OFFSET ?",
            (client_id, items_per_page, offset)
        )
        invoices = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) FROM invoices WHERE client_id = ?", (client_id,))
        total_invoices = cursor.fetchone()[0]
        total_pages = (total_invoices + items_per_page - 1) // items_per_page
        return {
            "invoices": invoices,
            "total_invoices": total_invoices,
            "total_pages": total_pages,
            "current_page": page,
            "items_per_page": items_per_page
        }

    except Exception as e:
        print(f"Erreur lors de la récupération des factures : {e}")
        return {
            "invoices": [],
            "total_invoices": 0,
            "total_pages": 0,
            "current_page": page,
            "items_per_page": items_per_page
        }
    finally:
        conn.close()