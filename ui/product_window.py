import tkinter as tk
from tkinter import messagebox
from products.products import *

def open_product_window():
    product_window = tk.Toplevel()
    product_window.title("Gestion des Produits")

    screen_width = product_window.winfo_screenwidth()
    screen_height = product_window.winfo_screenheight()
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.8)
    product_window.geometry(f"{window_width}x{window_height}")
    product_window.config(bg="#f7f7f7")

    title_frame = tk.Frame(product_window, bg="#f7f7f7", pady=10)
    title_frame.pack(fill="x", padx=20)

    title_label = tk.Label(
        title_frame,
        text="Gestion des Produits",
        font=("Arial", 26, "bold"),
        bg="#f7f7f7",
        fg="#2C3E50"
    )
    title_label.pack()
    # Cadre pour la recherche - positionné sous le titre mais au-dessus du cadre principal
    search_frame = tk.Frame(product_window, bg="#f7f7f7", pady=5)
    search_frame.pack(fill="x", padx=20, pady=(10, 0))  # Marges pour espacer légèrement

    search_var = tk.StringVar()

    tk.Label(
        search_frame, text="Nom du produit :", bg="#f7f7f7", font=("Arial", 14)
    ).pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 14))
    search_entry.pack(side="left", padx=5)
    tk.Button(
        search_frame,
        text="Chercher",
        command=lambda: search_product(),
        bg="#2980B9",
        fg="white",
        font=("Arial", 14),
    ).pack(side="left", padx=5)

    crud_frame = tk.Frame(product_window, bg="#f7f7f7", padx=20, pady=20)
    crud_frame.pack(pady=20, fill="both", expand=True)

    product_name_var = tk.StringVar()
    product_price_var = tk.StringVar()
    product_description_var = tk.StringVar()
    product_stock_var = tk.StringVar()  # Nouveau champ pour le stock

    items_per_page = 10
    current_page = 1
    product_database = []
  

    def add_product_ui():
        name = product_name_var.get()
        price = product_price_var.get()
        description = product_description_var.get()
        stock = product_stock_var.get()
        if name and price and description and stock:
            try:
                price = float(price)
                stock = int(stock)
                add_product(name, description, price, stock)
                product_name_var.set("")
                product_price_var.set("")
                product_description_var.set("")
                product_stock_var.set("")
                update_product_listbox()
                messagebox.showinfo("Succès", "Produit ajouté avec succès !")
            except ValueError:
                messagebox.showerror("Erreur", "Le prix et le stock doivent être des nombres valides.")
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

    def update_product_ui():
        selected_index = product_listbox.curselection()
        if selected_index:
            index = selected_index[0]-1
            product = product_database[index]
            name = product_name_var.get()
            price = product_price_var.get()
            description = product_description_var.get()
            stock = product_stock_var.get()
            if name and price and description and stock:
                try:
                    price = float(price)
                    stock = int(stock)
                    update_product(product[0], name, description, price, stock)
                    product_name_var.set("")
                    product_price_var.set("")
                    product_description_var.set("")
                    product_stock_var.set("")
                    update_product_listbox()
                    messagebox.showinfo("Succès", "Produit mis à jour avec succès !")
                except ValueError:
                    messagebox.showerror("Erreur", "Le prix et le stock doivent être des nombres valides.")
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à modifier.")

    def delete_product_ui():
        selected_index = product_listbox.curselection()
        if selected_index:
            index = selected_index[0]-1
            product = product_database[index]
            delete_product(product[0])
            update_product_listbox()
            messagebox.showinfo("Succès", "Produit supprimé avec succès !")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit à supprimer.")

    def update_product_listbox():
        # Supprimer les anciens produits affichés
        product_listbox.delete(0, tk.END)

        # Ajouter une ligne d'en-tête colorée
        header_text = "ID         Nom                         Description                  Prix (€)    Stock"
        product_listbox.insert(tk.END, header_text)
        product_listbox.itemconfig(0, bg="#D6EAF8", fg="#154360")  # Couleur de l'en-tête

         # Récupérer les produits et les afficher
        result = get_all_products(current_page , items_per_page)
        if search_var.get():
            result =filter_products_by_name(search_var.get(), current_page, items_per_page)
        products = result["products"]
         # Ajouter le produit à la base
        product_database.clear()
        for product in products:
            product_database.append(product)
        # Formatage de l'affichage des produits avec l'ID inclus
            product_text = f"{product[0]:<8}  {product[1]:<25}  {product[2]:<25}  {product[3]:<10.2f}  {product[4]}"
            product_listbox.insert(tk.END, product_text)

        #  Mettre à jour l'étiquette de pagination
        update_pagination_label(current_page,result["total_pages"])

    def update_pagination_label(current_page,total_pages):
        pagination_label.config(text=f"Page {current_page} sur {total_pages}")

    def next_page():
        nonlocal current_page
        result = get_all_products(current_page, items_per_page)
        if search_var.get():
            result =filter_products_by_name(search_var.get(), current_page, items_per_page)
        if current_page < result["total_pages"]:
            current_page += 1
            update_pagination_label(current_page,result["total_pages"])
            update_product_listbox()

    def previous_page():
        nonlocal current_page
        result = get_all_products(current_page, items_per_page)
        if search_var.get():
            result =filter_products_by_name(search_var.get(), current_page, items_per_page)
        if current_page > 1:
            current_page -= 1
            update_pagination_label(current_page,result["total_pages"])
            update_product_listbox()

    def on_product_select(event):
        selected_index = product_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0]-1
            product = product_database[index]
            product_name_var.set(product[1])
            product_description_var.set(product[2])
            product_price_var.set(product[3])
            product_stock_var.set(product[4])

    def search_product():
        search_query = search_var.get()
        nonlocal current_page
        current_page=1
        result = get_all_products(current_page, items_per_page)
        if search_query:
            # Filtrer les produits en fonction du nom
            result =filter_products_by_name(search_query, current_page, items_per_page)
            products = result["products"]
            # Ajouter le produit à la base
            for product in products:
                print(product)
            update_product_listbox()
            #update_pagination_label(current_page,result["total_pages"])
        else:
            # Si la barre de recherche est vide, afficher tous les produits
            update_product_listbox()
           # update_pagination_label(current_page,result["total_pages"])

    input_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(input_frame, text="Nom du produit :", bg="#f7f7f7", font=("Arial", 14)).grid(row=0, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=product_name_var, font=("Arial", 14)).grid(row=0, column=1, padx=10)

    tk.Label(input_frame, text="Description :", bg="#f7f7f7", font=("Arial", 14)).grid(row=1, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=product_description_var, font=("Arial", 14)).grid(row=1, column=1, padx=10)

    tk.Label(input_frame, text="Prix du produit :", bg="#f7f7f7", font=("Arial", 14)).grid(row=2, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=product_price_var, font=("Arial", 14)).grid(row=2, column=1, padx=10)

    tk.Label(input_frame, text="Stock :", bg="#f7f7f7", font=("Arial", 14)).grid(row=3, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=product_stock_var, font=("Arial", 14)).grid(row=3, column=1, padx=10)

    button_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    tk.Button(
        button_frame,
        text="Ajouter",
        command=add_product_ui,
        bg="#2980B9",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=0, padx=5)
    tk.Button(
        button_frame,
        text="Modifier",
        command=update_product_ui,
        bg="#27AE60",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=1, padx=5)
    tk.Button(
        button_frame,
        text="Supprimer",
        command=delete_product_ui,
        bg="#C0392B",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=2, padx=5)

    product_listbox = tk.Listbox(crud_frame, font=("Arial", 14), height=15)
    product_listbox.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
    product_listbox.bind("<<ListboxSelect>>", on_product_select)

    pagination_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    pagination_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Cadre pour la recherche

    tk.Button(
        pagination_frame,
        text="Précédent",
        command=previous_page,
        bg="#7F8C8D",
        fg="white",
        font=("Arial", 14),
    ).pack(side="left", padx=5)
    pagination_label = tk.Label(
        pagination_frame, text="", bg="#f7f7f7", font=("Arial", 14)
    )
    pagination_label.pack(side="left", padx=10)
    tk.Button(
        pagination_frame,
        text="Suivant",
        command=next_page,
        bg="#7F8C8D",
        fg="white",
        font=("Arial", 14),
    ).pack(side="left", padx=5)

    crud_frame.columnconfigure(0, weight=1)
    crud_frame.columnconfigure(1, weight=2)
    crud_frame.rowconfigure(0, weight=1)
    crud_frame.rowconfigure(1, weight=0)

    update_product_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_product_window()
    root.mainloop()