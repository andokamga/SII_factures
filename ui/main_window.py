import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from ui.product_window import open_product_window
from ui.invoice_window import open_invoice_window
from ui.client_window import open_client_window
from ui.register_window import open_register_window
from users.auth import get_username_from_file

def launch_main_window():
    # Fenêtre principale
    main_window = tk.Toplevel()
    main_window.title("Interface Principale")
    
    # Taille dynamique de la fenêtre (100% de l'écran)
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    window_width = int(screen_width * 1)
    window_height = int(screen_height * 1)
    main_window.geometry(f"{window_width}x{window_height}")
    main_window.state('zoomed')
    main_window.config(bg="#f7f7f7")  # Couleur de fond plus claire

    # Fonction pour obtenir la salutation en fonction de l'heure
    def get_greeting():
        current_hour = datetime.now().hour
        if current_hour < 12:
            return "Bonjour"
        elif current_hour < 18:
            return "Bon après-midi"
        else:
            return "Bonsoir"
    
    # Salutation à afficher
    greeting = get_greeting()

    # Cadre pour le nom de l'application et le bouton logout
    header_frame = tk.Frame(main_window, bg="#f7f7f7", pady=10)
    header_frame.pack(fill="x", padx=20)

    # Nom de l'application
    app_name_label = tk.Label(
        header_frame,
        text="SII Factures",
        font=("Arial", 26, "bold"),
        bg="#f7f7f7",
        fg="#2C3E50"
    )
    app_name_label.pack(side="left", padx=20)

    def logout():
        main_window.destroy()
        from ui.login_window import open_login_window
        open_login_window()

    # Bouton Logout
    logout_button = tk.Button(
        header_frame,
        text="Logout",
        font=("Arial", 14),
        bg="#FF5733",
        fg="white",
        relief="flat",
        bd=0,
        command=logout,
        height=2,
        width=10
    )
    logout_button.pack(side="right", padx=20)

    def on_logout_enter(event):
        logout_button.config(bg="#C0392B")  # Rouge plus foncé

    def on_logout_leave(event):
        logout_button.config(bg="#FF5733")  # Rouge d'origine

    logout_button.bind("<Enter>", on_logout_enter)
    logout_button.bind("<Leave>", on_logout_leave)

    # Salutation
    greeting_label = tk.Label(
        main_window, 
        text=f"{greeting} {get_username_from_file() or 'Utilisateur'}, bienvenue sur SII Factures !",
        font=("Arial", 20), 
        bg="#f7f7f7", 
        fg="#34495E"
    )
    greeting_label.pack(pady=20)

    # Cadre pour les boutons
    button_frame = tk.Frame(main_window, bg="#f7f7f7")
    button_frame.pack(pady=20)

    # Fonctions pour ouvrir les fenêtres spécifiques
    def open_user_management():
        open_register_window()

    def open_client():
        open_client_window()

    def open_product():
        open_product_window()

    def open_invoice():
        open_invoice_window()

    def open_invoice_management():
        open_product_window()

    def open_backup():
        open_invoice_window()

    # Boutons pour accéder aux différentes interfaces
    buttons = [
        ("Gestion des Utilisateurs", open_user_management),
        ("Gestion des Clients", open_client),
        ("Gestion des Produits", open_product),
        ("Création des Factures", open_invoice),
        ("Sauvegarde/Restauration", open_backup),
        ("Gestion des Factures", open_invoice_management)
    ]

    # Ajout des boutons dans une disposition en grille (2 colonnes)
    for i, (text, command) in enumerate(buttons):
        btn = tk.Button(
            button_frame,
            text=text,
            font=("Arial", 14),
            bg="#2980B9",
            fg="white",
            relief="solid",
            bd=1,
            width=30,
            height=2,
            command=command
        )
        btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)
    
            # Ajouter un effet de survol
        def on_enter(event, button=btn):
            button.config(bg="#1D5B89")  # Changer de couleur au survol

        def on_leave(event, button=btn):
            button.config(bg="#2980B9")  # Réinitialiser la couleur après le survol

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        # Copyright
    copyright_label = tk.Label(
        main_window,
        text="© 2025 SII Factures - Tous droits réservés.",
        font=("Arial", 12, "italic"),
        bg="#f7f7f7",
        fg="#7f8c8d"
    )
    copyright_label.pack(side="bottom", pady=10)

# Exemple pour tester
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    launch_main_window()
    root.mainloop()