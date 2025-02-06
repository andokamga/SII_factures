import tkinter as tk
from ui.main_window import launch_main_window
from users.auth import authenticate_user
import sys
import os
from tkinter import Tk, Label

def open_login_window():
    login_window = tk.Toplevel()
    login_window.title("Connexion")
    #icon = tk.PhotoImage(file="facture.png")
    #login_window.iconphoto(True, icon)
    # Taille de la fenêtre
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    window_width = int(screen_width * 1)
    window_height = int(screen_height * 1)
    login_window.geometry(f"{window_width}x{window_height}")
    login_window.state('zoomed')
    login_window.config(bg="#f0f0f0")
    login_window.resizable(True, True)
    
    # Frame centralisée
    frame = tk.Frame(login_window, bg="#ffffff", padx=40, pady=40, bd=3, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Titre
    title_label = tk.Label(frame, text="Connexion", font=("Arial", 20, "bold"), bg="#ffffff", fg="#007BFF")
    title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")
    
    # Champ Nom d'utilisateur
    tk.Label(frame, text="Nom d'utilisateur:", font=("Arial", 12), bg="#ffffff", fg="#007BFF").grid(row=1, column=0, pady=10, padx=10, sticky="e")
    username_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid", width=30)
    username_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")
    
    # Champ Mot de passe
    tk.Label(frame, text="Mot de passe:", font=("Arial", 12), bg="#ffffff", fg="#007BFF").grid(row=2, column=0, pady=10, padx=10, sticky="e")
    password_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid", width=30, show="*")
    password_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")
    
    # Gestion des événements de survol pour le bouton
    def on_enter(event):
        login_button.config(bg="#0056b3")
        
    def on_leave(event):
        login_button.config(bg="#007BFF")

    # Gestion de la connexion
    def handle_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        # Vérification des champs obligatoires
        if not username or not password:
            error_label.config(text="Tous les champs sont obligatoires.", fg="red")
            return
        
        # Authentification
        if authenticate_user(username, password):
            print("Connexion réussie")
            login_window.destroy()  # Fermer la fenêtre de connexion
            launch_main_window()  # Lancer la fenêtre principale
        else:
            error_label.config(text="Nom d'utilisateur ou mot de passe incorrect.", fg="red")
    
    # Bouton de connexion
    login_button = tk.Button(frame, text="Se connecter", font=("Arial", 12), bg="#007BFF", fg="white", relief="solid", bd=2, width=20, command=handle_login)
    login_button.grid(row=3, column=0, columnspan=2, pady=20, sticky="n")
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    # Label pour afficher des erreurs
    error_label = tk.Label(frame, text="", font=("Arial", 10), bg="#ffffff", fg="red")
    error_label.grid(row=4, column=0, columnspan=2, pady=5, sticky="n")

# Initialisation de la fenêtre principale
root = tk.Tk()
root.withdraw()  # Cacher la fenêtre principale pour ne montrer que la fenêtre de connexion
open_login_window()
root.mainloop()