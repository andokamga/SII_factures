import tkinter as tk

def open_register_window():
    register_window = tk.Toplevel()
    register_window.title("Inscription")

    tk.Label(register_window, text="Nom d'utilisateur:").grid(row=0, column=0, pady=5, padx=5)
    tk.Entry(register_window).grid(row=0, column=1, pady=5, padx=5)

    tk.Label(register_window, text="Mot de passe:").grid(row=1, column=0, pady=5, padx=5)
    tk.Entry(register_window, show="*").grid(row=1, column=1, pady=5, padx=5)

    tk.Label(register_window, text="Confirmer le mot de passe:").grid(row=2, column=0, pady=5, padx=5)
    tk.Entry(register_window, show="*").grid(row=2, column=1, pady=5, padx=5)

    tk.Button(register_window, text="S'inscrire", command=lambda: print("Inscription réussie")).grid(row=3, column=0, columnspan=2, pady=10)