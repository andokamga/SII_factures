import tkinter as tk
from ui.main_window import launch_main_window

def open_login_window():
    login_window = tk.Toplevel()
    login_window.title("Connexion")
    
    # Obtenez la taille de l'écran pour faire en sorte que la fenêtre soit presque en plein écran
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    
    # Définir la taille de la fenêtre proche du plein écran, en laissant un petit écart
    window_width = int(screen_width * 0.7)  # 70% de la largeur de l'écran
    window_height = int(screen_height * 0.7)  # 70% de la hauteur de l'écran
    login_window.geometry(f"{window_width}x{window_height}")  # Taille dynamique
    login_window.config(bg="#f0f0f0")  # Couleur de fond gris clair pour la fenêtre
    
    # Autoriser la fenêtre à être redimensionnée
    login_window.resizable(True, True)
    
    # Utilisation de Frame pour centrer les éléments dans un petit bloc
    frame = tk.Frame(login_window, bg="#ffffff", padx=40, pady=40, bd=3, relief="groove")  # Ajout d'un peu d'espace autour du formulaire
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Centrer le frame au centre de la fenêtre
    
    # Titre centralisé dans le frame
    title_label = tk.Label(frame, text="Connexion", font=("Arial", 20, "bold"), bg="#ffffff", fg="#007BFF")
    title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")
    
    # Label et champ "Nom d'utilisateur" avec allongement des champs
    tk.Label(frame, text="Nom d'utilisateur:", font=("Arial", 12), bg="#ffffff", fg="#007BFF").grid(row=1, column=0, pady=10, padx=10, sticky="e")
    username_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid", width=30)  # Largeur augmentée
    username_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")
    
    # Label et champ "Mot de passe" avec allongement des champs
    tk.Label(frame, text="Mot de passe:", font=("Arial", 12), bg="#ffffff", fg="#007BFF").grid(row=2, column=0, pady=10, padx=10, sticky="e")
    password_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid", width=30, show="*")  # Largeur augmentée
    password_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")
    
    # Bouton de connexion avec survol
    def on_enter(event):
        login_button.config(bg="#0056b3")
        
    def on_leave(event):
        login_button.config(bg="#007BFF")

    def handle_login():
        # Simuler une validation réussie
        print("Connexion réussie")
        login_window.destroy()  # Fermer la fenêtre de connexion
        launch_main_window()
        
    login_button = tk.Button(frame, text="Se connecter", font=("Arial", 12), bg="#007BFF", fg="white", relief="solid", bd=2, width=20, command= handle_login)
    login_button.grid(row=3, column=0, columnspan=2, pady=20, sticky="n")
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    # Option pour mot de passe oublié (facultatif)
    forgot_password_label = tk.Label(frame, text="Mot de passe oublié ?", font=("Arial", 10, "italic"), fg="#007BFF", bg="#ffffff", cursor="hand2")
    forgot_password_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="n")
    forgot_password_label.bind("<Button-1>", lambda e: print("Rediriger vers la récupération de mot de passe"))

# Initialisation de la fenêtre principale
root = tk.Tk()
root.withdraw()  # Cacher la fenêtre principale pour ne montrer que la fenêtre de connexion
open_login_window()
root.mainloop()