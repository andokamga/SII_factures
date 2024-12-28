import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def open_invoice_window():
    # Fenêtre de gestion des factures
    invoice_window = tk.Toplevel()
    invoice_window.title("Gestion des Factures")

    # Taille dynamique de la fenêtre (70% de l'écran)
    screen_width = invoice_window.winfo_screenwidth()
    screen_height = invoice_window.winfo_screenheight()
    window_width = int(screen_width * 0.7)
    window_height = int(screen_height * 0.7)
    invoice_window.geometry(f"{window_width}x{window_height}")
    invoice_window.config(bg="#f7f7f7")  # Couleur de fond claire

    # Cadre pour le titre
    title_frame = tk.Frame(invoice_window, bg="#ffffff", pady=10)
    title_frame.pack(fill="x", padx=20)

    title_label = tk.Label(
        title_frame,
        text="Gestion des Factures",
        font=("Arial", 26, "bold"),
        bg="#ffffff",
        fg="#2C3E50"
    )
    title_label.pack()

    # Cadre pour les fonctionnalités
    crud_frame = tk.Frame(invoice_window, bg="#f7f7f7", padx=20, pady=20)
    crud_frame.pack(pady=20, fill="both", expand=True)

    # Liste des clients et produits
    clients = ["Client 1", "Client 2", "Client 3"]
    products = [
        {"name": "Produit A", "price": 10.0},
        {"name": "Produit B", "price": 20.0},
        {"name": "Produit C", "price": 30.0}
    ]
    invoice_list = []

    # Widgets pour sélection des clients et produits
    tk.Label(crud_frame, text="Sélectionnez un client :", bg="#f7f7f7", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    client_combobox = ttk.Combobox(crud_frame, values=clients, font=("Arial", 12))
    client_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tk.Label(crud_frame, text="Sélectionnez un produit :", bg="#f7f7f7", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    product_combobox = ttk.Combobox(crud_frame, values=[p["name"] for p in products], font=("Arial", 12))
    product_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Liste des factures
    invoice_listbox = tk.Listbox(crud_frame, font=("Arial", 14), height=15)
    invoice_listbox.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

    # Générer une facture PDF
    def generate_pdf(invoice):
        file_name = f"{invoice['client']}_invoice.pdf"
        c = canvas.Canvas(file_name, pagesize=letter)
        c.drawString(100, 750, f"Facture pour: {invoice['client']}")
        c.drawString(100, 730, f"Produit: {invoice['product']}")
        c.drawString(100, 710, f"Prix: {invoice['price']} €")
        c.drawString(100, 690, f"Total: {invoice['price']} €")
        c.save()
        messagebox.showinfo("PDF Généré", f"La facture a été enregistrée sous le nom {file_name}.")

    # Ajouter une facture
    def add_invoice():
        client = client_combobox.get()
        product_name = product_combobox.get()

        if not client or not product_name:
            messagebox.showerror("Erreur", "Veuillez sélectionner un client et un produit.")
            return

        product = next((p for p in products if p["name"] == product_name), None)
        if not product:
            messagebox.showerror("Erreur", "Produit invalide.")
            return

        invoice = {
            "client": client,
            "product": product_name,
            "price": product["price"]
        }
        invoice_list.append(invoice)
        invoice_listbox.insert(tk.END, f"{client} - {product_name} - {product['price']} €")
        messagebox.showinfo("Succès", "Facture ajoutée avec succès.")

    # Imprimer une facture
    def print_invoice():
        selected_index = invoice_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_invoice = invoice_list[index]
            generate_pdf(selected_invoice)
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture à imprimer.")

    # Cadre des boutons
    button_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

    tk.Button(button_frame, text="Ajouter Facture", command=add_invoice, bg="#2980B9", fg="white", font=("Arial", 14)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Imprimer Facture", command=print_invoice, bg="#27AE60", fg="white", font=("Arial", 14)).pack(side="left", padx=5)

# Exemple pour tester
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    open_invoice_window()
    root.mainloop()