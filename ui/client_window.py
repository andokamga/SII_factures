import tkinter as tk

def open_client_window():
    client_window = tk.Toplevel()
    client_window.title("Gestion des Clients")

    tk.Label(client_window, text="Ajouter, Modifier ou Supprimer des Clients").pack(pady=10)