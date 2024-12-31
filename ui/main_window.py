import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from ui.product_window import open_product_window
from ui.invoice_window import open_invoice_window
from ui.client_window import open_client_window

def launch_main_window():
    # Fenêtre principale
    main_window = tk.Toplevel()
    main_window.title("Interface Principale")
    
    # Taille dynamique de la fenêtre (70% de l'écran)
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.8)
    main_window.geometry(f"{window_width}x{window_height}")
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
    
    # Cadre pour le nom de l'application à gauche et le bouton logout à droite
    header_frame = tk.Frame(main_window, bg="#f7f7f7", pady=10)
    header_frame.pack(fill="x", padx=20)  # Utilisation de fill="x" pour étendre horizontalement

    # Nom de l'application (placé à gauche)
    app_name_label = tk.Label(
        header_frame,
        text="SII Factures",
        font=("Arial", 26, "bold"),
        bg="#f7f7f7",
        fg="#2C3E50"  # Utilisation d'un bleu foncé pour le texte
    )
    app_name_label.pack(side="left", padx=20)  # Placer à gauche dans le cadre
    
    # Bouton Logout (placé à droite)
    logout_button = tk.Button(
        header_frame,
        text="Logout",
        font=("Arial", 14),
        bg="#FF5733",  # Utilisation d'un rouge plus vif
        fg="white",
        relief="flat",
        bd=0,
        command=main_window.destroy,
        height=2,
        width=10,
        highlightthickness=0,
    )
    
    # Fonction de survol pour changer la couleur du bouton
    def on_enter_logout(event, btn=logout_button):
        btn.config(bg="#F5B7B1")  # Change le fond en survol
    
    def on_leave_logout(event, btn=logout_button):
        btn.config(bg="#FF5733")  # Réinitialise la couleur de fond

    logout_button.bind("<Enter>", on_enter_logout)
    logout_button.bind("<Leave>", on_leave_logout)
    
    logout_button.pack(side="right", padx=20)  # Placer à droite dans le cadre

    # Affichage de la salutation (juste en dessous du nom de l'application)
    greeting_label = tk.Label(
        main_window, 
        text=f"{greeting}, utilisateur !", 
        font=("Arial", 20), 
        bg="#f7f7f7", 
        fg="#34495E"  # Utilisation d'une couleur gris-bleu pour le texte
    )
    greeting_label.pack(pady=20)

    # Cadre pour les boutons principaux
    button_frame = tk.Frame(main_window, bg="#f7f7f7", padx=20, pady=20)
    button_frame.pack(pady=20)  # Ajout d'un padding entre le cadre et le reste

    # Fonctions pour ouvrir les fenêtres spécifiques
    def open_user_management_window():
        messagebox.showinfo("Inscription", "Fenêtre d'inscription ouverte.")
        # Implémentez ici la logique pour ouvrir register_window.py

    def open_client():
        open_client_window()
        #messagebox.showinfo("Gestion des Clients", "Fenêtre de gestion des clients ouverte.")
        # Implémentez ici la logique pour ouvrir client_window.py

    def open_product():
        open_product_window()
        #messagebox.showinfo("Gestion des Produits", "Fenêtre de gestion des produits/services ouverte.")
        # Implémentez ici la logique pour ouvrir product_window.py

    def open_invoice():
        open_invoice_window()
        #messagebox.showinfo("Gestion des Factures", "Fenêtre de gestion des factures ouverte.")
        # Implémentez ici la logique pour ouvrir invoice_window.py

    # Boutons pour accéder aux différentes interfaces
    buttons = [
    ("Gestion des Utilisateurs", open_user_management_window),
        ("Gestion des Clients", open_client),
        ("Gestion des Produits/Services", open_product),
        ("Gestion des Factures", open_invoice),
    ]

    for text, command in buttons:
        btn = tk.Button(
            button_frame,
            text=text,
            font=("Arial", 14),
            bg="#2980B9",  # Utilisation d'un bleu moyen pour les boutons
            fg="white",
            relief="solid",  # Bordure solide
            bd=1,  # Bordure fine
            width=30,
            height=2,
            command=command,
            highlightthickness=0,  # Pas de surbrillance par défaut
            padx=10,
            pady=5
        )
        # Appliquer des bords arrondis en utilisant une méthode externe
        btn.config(
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#2980B9",
            activebackground="#1D5B89",  # Fond au survol plus foncé
            activeforeground="white"
        )
        btn.pack(pady=10, padx=5)  # Padding horizontal et vertical pour espacement
        
        # Effet de survol sur les boutons
        def on_enter(event, btn=btn):
            btn.config(bg="#1D5B89")  # Change le fond en survol
        def on_leave(event, btn=btn):
            btn.config(bg="#2980B9")  # Réinitialise la couleur de fond

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

# Exemple pour tester
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale pour n'afficher que la fenêtre secondaire
    launch_main_window()
    root.mainloop()