import tkinter as tk
from tkinter import messagebox

def open_product_window():
    # Fenêtre de gestion des produits
    product_window = tk.Toplevel()
    product_window.title("Gestion des Produits")
    
    # Taille dynamique de la fenêtre (70% de l'écran)
    screen_width = product_window.winfo_screenwidth()
    screen_height = product_window.winfo_screenheight()
    window_width = int(screen_width * 0.7)
    window_height = int(screen_height * 0.7)
    product_window.geometry(f"{window_width}x{window_height}")
    product_window.config(bg="#f7f7f7")  # Couleur de fond claire

    # Cadre pour le titre
    title_frame = tk.Frame(product_window, bg="#ffffff", pady=10)
    title_frame.pack(fill="x", padx=20)

    title_label = tk.Label(
        title_frame,
        text="Gestion des Produits",
        font=("Arial", 26, "bold"),
        bg="#ffffff",
        fg="#2C3E50"
    )
    title_label.pack()

    # Cadre pour les fonctionnalités
    crud_frame = tk.Frame(product_window, bg="#f7f7f7", padx=20, pady=20)
    crud_frame.pack(pady=20, fill="both", expand=True)

    # Variables pour les champs d'entrée
    product_name_var = tk.StringVar()
    product_price_var = tk.StringVar()

    # Exemple de liste de produits
    product_list = [{"name": f"Produit {i}", "price": round(10 + i * 2.5, 2)} for i in range(1, 101)]
    
    items_per_page = 10  # Nombre d'éléments par page
    current_page = 0     # Page actuelle

    # Fonctionnalités CRUD
    def add_product():
        name = product_name_var.get()
        price = product_price_var.get()
        if name and price:
            try:
                price = float(price)
                product_list.append({"name": name, "price": price})
                product_name_var.set("")
                product_price_var.set("")
                update_product_listbox()
                messagebox.showinfo("Succès", "Produit ajouté avec succès !")
            except ValueError:
                messagebox.showerror("Erreur", "Le prix doit être un nombre valide.")
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

    def update_product():
        selected_index = product_listbox.curselection()
        if selected_index:
            index = current_page * items_per_page + selected_index[0]
            name = product_name_var.get()
            price = product_price_var.get()
            if name and price:
                try:
                    price = float(price)
                    product_list[index] = {"name": name, "price": price}
                    product_name_var.set("")
                    product_price_var.set("")
                    update_product_listbox()
                    messagebox.showinfo("Succès", "Produit mis à jour avec succès !")
                except ValueError:
                    messagebox.showerror("Erreur", "Le prix doit être un nombre valide.")
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à modifier.")

    def delete_product():
        selected_index = product_listbox.curselection()
        if selected_index:
            index = current_page * items_per_page + selected_index[0]
            product_list.pop(index)
            update_product_listbox()
            messagebox.showinfo("Succès", "Produit supprimé avec succès !")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à supprimer.")

    def update_product_listbox():
        product_listbox.delete(0, tk.END)
        start_index = current_page * items_per_page
        end_index = min(start_index + items_per_page, len(product_list))
        for product in product_list[start_index:end_index]:
            product_listbox.insert(tk.END, f"{product['name']} - {product['price']:.2f} €")
        update_pagination_label()

    def update_pagination_label():
        total_pages = (len(product_list) + items_per_page - 1) // items_per_page
        pagination_label.config(text=f"Page {current_page + 1} sur {total_pages}")

    def next_page():
        nonlocal current_page
        if (current_page + 1) * items_per_page < len(product_list):
            current_page += 1
            update_product_listbox()

    def previous_page():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            update_product_listbox()

    def on_product_select(event):
        selected_index = product_listbox.curselection()
        if selected_index:
            index = current_page * items_per_page + selected_index[0]
            selected_product = product_list[index]
            product_name_var.set(selected_product["name"])
            product_price_var.set(selected_product["price"])
    

    # Entrées utilisateur pour les produits
    input_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(input_frame, text="Nom du produit :", bg="#f7f7f7", font=("Arial", 14)).grid(row=0, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=product_name_var, font=("Arial", 14)).grid(row=0, column=1, padx=10)

    tk.Label(input_frame, text="Prix du produit :", bg="#f7f7f7", font=("Arial", 14)).grid(row=1, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=product_price_var, font=("Arial", 14)).grid(row=1, column=1, padx=10)

    # Boutons CRUD
    button_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    tk.Button(button_frame, text="Ajouter", command=add_product, bg="#2980B9", fg="white", font=("Arial", 14), width=15).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Modifier", command=update_product, bg="#27AE60", fg="white", font=("Arial", 14), width=15).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Supprimer", command=delete_product, bg="#C0392B", fg="white", font=("Arial", 14), width=15).grid(row=0, column=2, padx=5)

    # Liste des produits
    product_listbox = tk.Listbox(crud_frame, font=("Arial", 14), height=15)
    product_listbox.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
    product_listbox.bind("<<ListboxSelect>>", on_product_select)

    # Pagination
    pagination_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    pagination_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    tk.Button(pagination_frame, text="Précédent", command=previous_page, bg="#7F8C8D", fg="white", font=("Arial", 14)).pack(side="left", padx=5)
    pagination_label = tk.Label(pagination_frame, text="", bg="#f7f7f7", font=("Arial", 14))
    pagination_label.pack(side="left", padx=10)
    tk.Button(pagination_frame, text="Suivant", command=next_page, bg="#7F8C8D", fg="white", font=("Arial", 14)).pack(side="left", padx=5)

    # Configuration des proportions
    crud_frame.columnconfigure(0, weight=1)
    crud_frame.columnconfigure(1, weight=2)
    crud_frame.rowconfigure(0, weight=1)
    crud_frame.rowconfigure(1, weight=0)

    # Mise à jour initiale de la liste
    update_product_listbox()

# Exemple pour tester
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    open_product_window()
    root.mainloop()