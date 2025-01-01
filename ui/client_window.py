import tkinter as tk
from tkinter import messagebox
from clients.clients import *

def open_client_window():
    client_window = tk.Toplevel()
    client_window.title("Gestion des Clients")

    # Set window size based on screen dimensions
    screen_width = client_window.winfo_screenwidth()
    screen_height = client_window.winfo_screenheight()
    window_width = int(screen_width * 1)
    window_height = int(screen_height * 1)
    client_window.geometry(f"{window_width}x{window_height}")
    client_window.state('zoomed')
    client_window.config(bg="#f7f7f7")

    # Title Frame
    title_frame = tk.Frame(client_window, bg="#f7f7f7", pady=10)
    title_frame.pack(fill="x", padx=20)

    title_label = tk.Label(
        title_frame,
        text="Gestion des Clients",
        font=("Arial", 26, "bold"),
        bg="#f7f7f7",
        fg="#2C3E50"
    )
    title_label.pack()

    # Search Frame (for client search)
    search_frame = tk.Frame(client_window, bg="#f7f7f7", pady=5)
    search_frame.pack(fill="x", padx=20, pady=(10, 0))

    search_var = tk.StringVar()

    tk.Label(
        search_frame, text="Téléphone :", bg="#f7f7f7", font=("Arial", 14)
    ).pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 14))
    search_entry.pack(side="left", padx=5)
    tk.Button(
        search_frame,
        text="Chercher",
        command=lambda: search_client(),
        bg="#2980B9",
        fg="white",
        font=("Arial", 14),
    ).pack(side="left", padx=5)

    # CRUD Frame for client operations
    crud_frame = tk.Frame(client_window, bg="#f7f7f7", padx=20, pady=20)
    crud_frame.pack(pady=20, fill="both", expand=True)

    client_name_var = tk.StringVar()
    client_email_var = tk.StringVar()
    client_phone_var = tk.StringVar()
    client_address_var = tk.StringVar()

    items_per_page = 20
    current_page = 1
    client_database = []

    def add_client_ui():
        name = client_name_var.get()
        email = client_email_var.get()
        phone = client_phone_var.get()
        address = client_address_var.get()
        if name and email and phone and address:
            add_client(name, email, phone, address)
            client_name_var.set("")
            client_email_var.set("")
            client_phone_var.set("")
            client_address_var.set("")
            update_client_listbox()
            messagebox.showinfo("Succès", "Client ajouté avec succès !")
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

    def update_client_ui():
        selected_index = client_listbox.curselection()
        if selected_index:
            index = selected_index[0] - 1
            client = client_database[index]
            name = client_name_var.get()
            email = client_email_var.get()
            phone = client_phone_var.get()
            address = client_address_var.get()
            if name and email and phone and address:
                update_client(client[0], name, email, phone, address)
                client_name_var.set("")
                client_email_var.set("")
                client_phone_var.set("")
                client_address_var.set("")
                update_client_listbox()
                messagebox.showinfo("Succès", "Client mis à jour avec succès !")
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un client à modifier.")

    def delete_client_ui():
        selected_index = client_listbox.curselection()
        if selected_index:
            index = selected_index[0] - 1
            client = client_database[index]
            delete_client(client[0])
            update_client_listbox()
            messagebox.showinfo("Succès", "Client supprimé avec succès !")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un client à supprimer.")

    def update_client_listbox():
        # Clear the existing client list
        client_listbox.delete(0, tk.END)

        # Add header row
        header_text = "ID       Nom                               Email                             Téléphone                 Adresse"
        client_listbox.insert(tk.END, header_text)
        client_listbox.itemconfig(0, bg="#D6EAF8", fg="#154360")  # Header color

        # Fetch and display clients
        result = get_all_clients(current_page, items_per_page)
        if search_var.get():
            result = filter_clients_by_phone(search_var.get(), current_page, items_per_page)
        clients = result["clients"]
        client_database.clear()
        for client in clients:
            client_database.append(client)
            client_text = f"{client[0]:<8}  {client[1]:<25}  {client[2]:<30}  {client[3]:<20}  {client[4]}"
            client_listbox.insert(tk.END, client_text)

        # Update pagination label
        update_pagination_label(current_page, result["total_pages"])

    def update_pagination_label(current_page, total_pages):
        pagination_label.config(text=f"Page {current_page} sur {total_pages}")

    def next_page():
        nonlocal current_page
        result = get_all_clients(current_page, items_per_page)
        if search_var.get():
            result = filter_clients_by_phone(search_var.get(), current_page, items_per_page)
        if current_page < result["total_pages"]:
            current_page += 1
            update_pagination_label(current_page, result["total_pages"])
            update_client_listbox()

    def previous_page():
        nonlocal current_page
        result = get_all_clients(current_page, items_per_page)
        if search_var.get():
            result = filter_clients_by_phone(search_var.get(), current_page, items_per_page)
        if current_page > 1:
            current_page -= 1
            update_pagination_label(current_page, result["total_pages"])
            update_client_listbox()

    def on_client_select(event):
        selected_index = client_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0] - 1
            client = client_database[index]
            client_name_var.set(client[1])
            client_email_var.set(client[2])
            client_phone_var.set(client[3])
            client_address_var.set(client[4])

    def search_client():
        search_query = search_var.get()
        nonlocal current_page
        current_page = 1
        result = get_all_clients(current_page, items_per_page)
        if search_query:
            result = filter_clients_by_phone(search_query, current_page, items_per_page)
            update_client_listbox()
        else:
            update_client_listbox()

    input_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(input_frame, text="Nom du client :", bg="#f7f7f7", font=("Arial", 14)).grid(row=0, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=client_name_var, font=("Arial", 14)).grid(row=0, column=1, padx=10)

    tk.Label(input_frame, text="Email :", bg="#f7f7f7", font=("Arial", 14)).grid(row=1, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=client_email_var, font=("Arial", 14)).grid(row=1, column=1, padx=10)

    tk.Label(input_frame, text="Téléphone :", bg="#f7f7f7", font=("Arial", 14)).grid(row=2, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=client_phone_var, font=("Arial", 14)).grid(row=2, column=1, padx=10)

    tk.Label(input_frame, text="Adresse :", bg="#f7f7f7", font=("Arial", 14)).grid(row=3, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=client_address_var, font=("Arial", 14)).grid(row=3, column=1, padx=10)

    button_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    tk.Button(
        button_frame,
        text="Ajouter",
        command=add_client_ui,
        bg="#2980B9",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=0, padx=5)
    tk.Button(
        button_frame,
        text="Modifier",
        command=update_client_ui,
        bg="#27AE60",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=1, padx=5)
    tk.Button(
        button_frame,
        text="Supprimer",
        command=delete_client_ui,
        bg="#C0392B",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=2, padx=5)

    client_listbox = tk.Listbox(crud_frame, font=("Arial", 14), height=15)
    client_listbox.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
    client_listbox.bind("<<ListboxSelect>>", on_client_select)

    pagination_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    pagination_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

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

    update_client_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_client_window()
    root.mainloop()