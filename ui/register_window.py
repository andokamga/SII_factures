import tkinter as tk
from tkinter import messagebox
from users.users import *

def open_register_window():
    register_window = tk.Toplevel()
    register_window.title("Gestion des Utilisateurs")

    # Set window size based on screen dimensions
    screen_width = register_window.winfo_screenwidth()
    screen_height = register_window.winfo_screenheight()
    window_width = int(screen_width * 1)
    window_height = int(screen_height * 1)
    register_window.geometry(f"{window_width}x{window_height}")
    register_window.state('zoomed')
    register_window.config(bg="#f7f7f7")

    # Title Frame
    title_frame = tk.Frame(register_window, bg="#f7f7f7", pady=10)
    title_frame.pack(fill="x", padx=20)

    title_label = tk.Label(
        title_frame,
        text="Gestion des Utilisateurs",
        font=("Arial", 26, "bold"),
        bg="#f7f7f7",
        fg="#2C3E50"
    )
    title_label.pack()

    # Search Frame (for user search)
    search_frame = tk.Frame(register_window, bg="#f7f7f7", pady=5)
    search_frame.pack(fill="x", padx=20, pady=(10, 0))

    search_var = tk.StringVar()

    tk.Label(
        search_frame, text="Nom d'utilisateur :", bg="#f7f7f7", font=("Arial", 14)
    ).pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 14))
    search_entry.pack(side="left", padx=5)
    tk.Button(
        search_frame,
        text="Chercher",
        command=lambda: search_user(),
        bg="#2980B9",
        fg="white",
        font=("Arial", 14),
    ).pack(side="left", padx=5)

    # CRUD Frame for user operations
    crud_frame = tk.Frame(register_window, bg="#f7f7f7", padx=20, pady=20)
    crud_frame.pack(pady=20, fill="both", expand=True)

    user_name_var = tk.StringVar()
    user_password_var = tk.StringVar()
    user_role_var = tk.StringVar()

    items_per_page = 20
    current_page = 1
    user_database = []

    def add_user_ui():
        username = user_name_var.get()
        password = user_password_var.get()
        role = user_role_var.get()
        if username and password and role:
            add_user(username, password, role)
            user_name_var.set("")
            user_password_var.set("")
            user_role_var.set("")
            update_user_listbox()
            messagebox.showinfo("Succès", "Utilisateur ajouté avec succès !")
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

    def update_user_ui():
        selected_index = user_listbox.curselection()
        if selected_index:
            index = selected_index[0] - 1
            user = user_database[index]
            username = user_name_var.get()
            password = user_password_var.get()
            role = user_role_var.get()
            if username and password and role:
                update_user(user[0], username, password, role)
                user_name_var.set("")
                user_password_var.set("")
                user_role_var.set("")
                update_user_listbox()
                messagebox.showinfo("Succès", "Utilisateur mis à jour avec succès !")
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un utilisateur à modifier.")

    def delete_user_ui():
        selected_index = user_listbox.curselection()
        if selected_index:
            index = selected_index[0] - 1
            user = user_database[index]
            delete_user(user[0])
            update_user_listbox()
            messagebox.showinfo("Succès", "Utilisateur supprimé avec succès !")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un utilisateur à supprimer.")

    def update_user_listbox():
        # Clear the existing user list
        user_listbox.delete(0, tk.END)

        # Add header row
        header_text = "ID       Nom d'utilisateur                Rôle"
        user_listbox.insert(tk.END, header_text)
        user_listbox.itemconfig(0, bg="#D6EAF8", fg="#154360")  # Header color

        # Fetch and display users
        result = get_all_users(current_page, items_per_page)
        if search_var.get():
            result = filter_users_by_username(search_var.get(), current_page, items_per_page)
        users = result["users"]
        user_database.clear()
        for user in users:
            user_database.append(user)
            user_text = f"{user[0]:<8}  {user[1]:<30}  {user[3]}"
            user_listbox.insert(tk.END, user_text)

        # Update pagination label
        update_pagination_label(current_page, result["total_pages"])

    def update_pagination_label(current_page, total_pages):
        pagination_label.config(text=f"Page {current_page} sur {total_pages}")

    def next_page():
        nonlocal current_page
        result = get_all_users(current_page, items_per_page)
        if search_var.get():
            result = filter_users_by_username(search_var.get(), current_page, items_per_page)
        if current_page < result["total_pages"]:
            current_page += 1
            update_pagination_label(current_page, result["total_pages"])
            update_user_listbox()

    def previous_page():
        nonlocal current_page
        result = get_all_users(current_page, items_per_page)
        if search_var.get():
            result = filter_users_by_username(search_var.get(), current_page, items_per_page)
        if current_page > 1:
            current_page -= 1
            update_pagination_label(current_page, result["total_pages"])
            update_user_listbox()

    def on_user_select(event):
        selected_index = user_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0] - 1
            user = user_database[index]
            user_name_var.set(user[1])
            user_password_var.set(user[2])
            user_role_var.set(user[3])

    def search_user():
        search_query = search_var.get()
        nonlocal current_page
        current_page = 1
        result = get_all_users(current_page, items_per_page)
        if search_query:
            result = filter_users_by_username(search_query, current_page, items_per_page)
            update_user_listbox()
        else:
            update_user_listbox()

    input_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(input_frame, text="Nom d'utilisateur :", bg="#f7f7f7", font=("Arial", 14)).grid(row=0, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=user_name_var, font=("Arial", 14)).grid(row=0, column=1, padx=10)

    tk.Label(input_frame, text="Mot de passe :", bg="#f7f7f7", font=("Arial", 14)).grid(row=1, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=user_password_var, font=("Arial", 14), show="*").grid(row=1, column=1, padx=10)

    tk.Label(input_frame, text="Rôle :", bg="#f7f7f7", font=("Arial", 14)).grid(row=2, column=0, sticky="w")
    tk.Entry(input_frame, textvariable=user_role_var, font=("Arial", 14)).grid(row=2, column=1, padx=10)

    button_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    tk.Button(
        button_frame,
        text="Ajouter",
        command=add_user_ui,
        bg="#2980B9",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=0, padx=5)
    tk.Button(
        button_frame,
        text="Modifier",
        command=update_user_ui,
        bg="#27AE60",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=1, padx=5)
    tk.Button(
        button_frame,
        text="Supprimer",
        command=delete_user_ui,
        bg="#C0392B",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=2, padx=5)

    user_listbox = tk.Listbox(crud_frame, font=("Arial", 14), height=15)
    user_listbox.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
    user_listbox.bind("<<ListboxSelect>>", on_user_select)

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

    update_user_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_register_window()
    root.mainloop()