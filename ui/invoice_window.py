import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
import random
from clients.clients import *
from products.products import *

import tkinter as tk
from tkinter import ttk, messagebox

import tkinter as tk
from tkinter import ttk, messagebox

def open_invoice_window(): 
    # Window Setup
    invoice_window = tk.Toplevel()
    invoice_window.title("Gestion des Factures")

    screen_width = invoice_window.winfo_screenwidth()
    screen_height = invoice_window.winfo_screenheight()
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.8)
    invoice_window.geometry(f"{window_width}x{window_height}")
    invoice_window.config(bg="#f7f7f7")

    # Title Frame
    title_frame = tk.Frame(invoice_window, bg="#f7f7f7", pady=10)
    title_frame.pack(fill="x", padx=20)
    title_label = tk.Label(
        title_frame,
        text="Gestion des Factures",
        font=("Arial", 26, "bold"),
        bg="#f7f7f7",
        fg="#2C3E50"
    )
    title_label.pack()

    # Variables and Data
    client_search_var = tk.StringVar()
    product_search_var = tk.StringVar()
    selected_client_var = tk.StringVar()
    invoice_id_var = tk.StringVar()
    tax_percentage_var = tk.StringVar(value="0")
    client_id = 0
    client_phone = ""
    invoice_items = []  # Liste des produits ajoutés à une facture
    invoices_db = []  # Base de données des factures
    products_db = []

    # Search Client Section
    search_frame = tk.Frame(invoice_window, bg="#f7f7f7", pady=5)
    search_frame.pack(fill="x", padx=20, pady=(10, 0))
    tk.Label(search_frame, text="Téléphone du client :", bg="#f7f7f7", font=("Arial", 14)).pack(side="left", padx=5)
    tk.Entry(search_frame, textvariable=client_search_var, font=("Arial", 14), width=20).pack(side="left", padx=5)
    tk.Button(
        search_frame,
        text="Chercher",
        command=lambda: search_client(),
        bg="#2980B9",
        fg="white",
        font=("Arial", 14),
    ).pack(side="left", padx=5)
    tk.Label(search_frame, textvariable=selected_client_var, bg="#f7f7f7", font=("Arial", 14, "italic")).pack(side="left", padx=20)

    def search_client():
        nonlocal client_id
        nonlocal client_phone
        search_query = client_search_var.get().strip()

        if not search_query:
            selected_client_var.set("Aucun client trouvé")
            messagebox.showerror("Erreur", "Veuillez entrer un numéro de téléphone valide.")
            return

        try:
        # Appeler la fonction pour filtrer les clients
            result = filter_clients_by_phone(search_query, 1, 1)
            clients = result["clients"]

        # Vérifier si des clients ont été trouvés
            if clients:
                client_id = clients[0][0]
                client_phone = clients[0][3]
                client_name = clients[0][1]

            # Mettre à jour l'interface utilisateur avec les informations du client
                selected_client_var.set(f"Client trouvé : {client_name} - {client_phone}")
            else:
            # Si aucun client n'est trouvé
                client_id = None
                client_phone = None
                selected_client_var.set("Aucun client trouvé")
                messagebox.showinfo("Résultat", "Aucun client correspondant n'a été trouvé.")
        except Exception as e:
        # Gérer les erreurs éventuelles
            selected_client_var.set("Erreur lors de la recherche du client")
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la recherche : {e}")

    # Section pourcentage de taxe
    tax_frame = tk.Frame(invoice_window, bg="#f7f7f7", pady=5)
    tax_frame.pack(fill="x", padx=20, pady=(5, 0))
    tk.Label(tax_frame, text="Pourcentage de taxe (%):", bg="#f7f7f7", font=("Arial", 14)).pack(side="left", padx=5)
    tk.Entry(tax_frame, textvariable=tax_percentage_var, font=("Arial", 14), width=5).pack(side="left", padx=5)

    # Vérification et mise à jour du total avec taxes
    def calculate_total_with_tax():
        try:
            tax_percentage = float(tax_percentage_var.get())
            if tax_percentage < 0:
                raise ValueError("Le pourcentage de taxe ne peut pas être négatif.")
            total = sum(item["total"] for item in invoice_items)
            total_with_tax = total + (total * tax_percentage / 100)
            return total_with_tax
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un pourcentage de taxe valide.")
            return None
        
    def calculate_total_tax():
        try:
            tax_percentage = float(tax_percentage_var.get())
            if tax_percentage < 0:
                raise ValueError("Le pourcentage de taxe ne peut pas être négatif.")
            total = sum(item["total"] for item in invoice_items)
            total_tax = (total * tax_percentage / 100)
            return total_tax
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un pourcentage de taxe valide.")
            return None

    # CRUD Factures Section
    crud_frame = tk.Frame(invoice_window, bg="#f7f7f7", padx=20, pady=20)
    crud_frame.pack(pady=20, fill="both", expand=True)

    # Invoice List
    invoice_listbox = tk.Listbox(crud_frame, font=("Arial", 14), height=15)
    invoice_listbox.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

    def update_invoice_listbox():
        invoice_listbox.delete(0, tk.END)

        # Add header row
        header_text = "Id       Client                               Tax                            Total"
        invoice_listbox.insert(tk.END, header_text)
        invoice_listbox.itemconfig(0, bg="#D6EAF8", fg="#154360")  # Header color

        for invoice in invoices_db:
            invoice_text = f"{invoice['id']:<8} {invoice['client']:<25} {invoice['tax']:.2f}€                     {invoice['total']:.2f}€"
            invoice_listbox.insert(tk.END, invoice_text)


    # Invoice Actions
    def add_invoice():
        if not selected_client_var.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un client.")
            return
        if not invoice_items:
            messagebox.showerror("Erreur", "Aucun produit ajouté.")
            return

        invoice = {
            "id": client_id,
            "client": client_phone,
            "tax": calculate_total_tax(),
            "items": invoice_items.copy(),
            "total": calculate_total_with_tax()
        }
        invoices_db.append(invoice)
        messagebox.showinfo("Succès", "Facture ajoutée avec succès.")
        reset_invoice()
        update_invoice_listbox()

    def edit_invoice():
        selected_index = invoice_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            invoice = invoices_db[index]
            selected_client_var.set(invoice["client"])
            invoice_items.clear()
            invoice_items.extend(invoice["items"])
            update_invoice_items_tree()
            invoice_id_var.set(invoice["id"])
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture à modifier.")

    def delete_invoice():
        selected_index = invoice_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            invoices_db.pop(index)
            messagebox.showinfo("Succès", "Facture supprimée.")
            update_invoice_listbox()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture à supprimer.")

    def reset_invoice():
        selected_client_var.set("")
        invoice_items.clear()
        update_invoice_items_tree()
        invoice_id_var.set("")

    # Invoice Items Section
    items_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    items_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Treeview for Invoice Items
    items_tree = ttk.Treeview(items_frame, columns=("Name", "Price", "Quantity", "Total"), show="headings", height=10)
    items_tree.pack(fill="both", expand=True)

    items_tree.heading("Name", text="Produit")
    items_tree.heading("Price", text="Prix Unitaire (€)")
    items_tree.heading("Quantity", text="Quantité")
    items_tree.heading("Total", text="Total (€)")
    items_tree.column("Name", width=200)
    items_tree.column("Price", width=100)
    items_tree.column("Quantity", width=100)
    items_tree.column("Total", width=100)

    def update_invoice_items_tree():
        for row in items_tree.get_children():
            items_tree.delete(row)
        for item in invoice_items:
            items_tree.insert("", "end", values=(item["name"], f"{item['price']:.2f}", item["quantity"], f"{item['total']:.2f}"))

    def add_product_to_invoice(product_name, product_price):
        for item in invoice_items:
            if item["name"] == product_name:
                item["quantity"] += 1
                item["total"] = item["quantity"] * item["price"]
                update_invoice_items_tree()
                return
        invoice_items.append({"name": product_name, "price": product_price, "quantity": 1, "total": product_price})
        update_invoice_items_tree()

    def modify_product_quantity(item_name, quantity_change):
        for item in invoice_items:
            if item["name"] == item_name:
                item["quantity"] += quantity_change
                if item["quantity"] < 1:
                    item["quantity"] = 1
                item["total"] = item["quantity"] * item["price"]
                update_invoice_items_tree()
                return
        messagebox.showerror("Erreur", "Produit non trouvé dans la facture.")

    # Product Search Section
    search_product_frame = tk.Frame(invoice_window, bg="#f7f7f7", pady=5)
    search_product_frame.pack(fill="x", padx=20, pady=(10, 0))

    # Move search product frame above products_frame
    tk.Label(search_product_frame, text="Rechercher un produit :", bg="#f7f7f7", font=("Arial", 14)).pack(side="left", padx=5)
    tk.Entry(search_product_frame, textvariable=product_search_var, font=("Arial", 14), width=20).pack(side="left", padx=5)

    def search_product():
        products_db.clear()
        search_query = product_search_var.get().strip().lower()
        product_listbox.delete(0, tk.END)
        products = filter_products_by_name(search_query, 1, 5)["products"]
        if products: 
            for product in products:
                products_db.append(product)
        for product in products_db:
            product_listbox.insert(tk.END, f"{product[1]} - {product[3]}€")

    tk.Button(search_product_frame, text="Chercher", command=search_product, bg="#2980B9", fg="white", font=("Arial", 14)).pack(side="left", padx=5)

    # Available Products Section
    products_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    products_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(products_frame, text="Produits :", bg="#f7f7f7", font=("Arial", 14)).pack(side="top", anchor="w")
    product_listbox = tk.Listbox(products_frame, font=("Arial", 14), height=5)
    product_listbox.pack(fill="both", expand=True)

    def update_products_listbox():
        product_listbox.delete(0, tk.END)
        for product in products_db:
            product_listbox.insert(tk.END, f"{product['name']} - {product['price']}€")

    def select_product(event):
        selected_index = product_listbox.curselection()
        if selected_index:
            product = products_db[selected_index[0]]
            add_product_to_invoice(product[1], product[3])

    product_listbox.bind("<<ListboxSelect>>", select_product)
    update_products_listbox()

    # Invoice Action Buttons
    action_frame = tk.Frame(invoice_window, bg="#f7f7f7")
    action_frame.pack(pady=20)

    tk.Button(action_frame, text="Ajouter Facture", font=("Arial", 14), bg="#27AE60", fg="white", command=add_invoice).pack(side="left", padx=10)
    tk.Button(action_frame, text="Modifier Facture", font=("Arial", 14), bg="#2980B9", fg="white", command=edit_invoice).pack(side="left", padx=10)
    tk.Button(action_frame, text="Supprimer Facture", font=("Arial", 14), bg="#C0392B", fg="white", command=delete_invoice).pack(side="left", padx=10)
    tk.Button(action_frame, text="Imprimer Facture", font=("Arial", 14), bg="#7ED957", fg="black", command=delete_invoice).pack(side="left", padx=10)

    # Frame Configuration
    crud_frame.columnconfigure(0, weight=1)
    crud_frame.columnconfigure(1, weight=2)
    crud_frame.rowconfigure(0, weight=1)
    crud_frame.rowconfigure(1, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_invoice_window()
    root.mainloop()