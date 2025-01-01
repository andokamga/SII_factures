import tkinter as tk
import os
import shutil
from tkinter import messagebox, filedialog
from restauration.restauration import *

def open_backup_restore_window():
    window = tk.Toplevel()
    window.title("Gestion des Sauvegardes et Restauration")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = int(screen_width * 1)
    window_height = int(screen_height * 1)
    window.geometry(f"{window_width}x{window_height}")
    window.state("zoomed")
    window.config(bg="#f7f7f7")

    # Titre
    title_frame = tk.Frame(window, bg="#f7f7f7", pady=10)
    title_frame.pack(fill="x", padx=20)

    title_label = tk.Label(
        title_frame,
        text="Gestion des Sauvegardes et Restauration",
        font=("Arial", 26, "bold"),
        bg="#f7f7f7",
        fg="#2C3E50"
    )
    title_label.pack()

    # Variables et pagination
    items_per_page = 20
    current_page = 1
    backups = []

    # Fonctions internes
    def update_backup_listbox():
        """Met à jour la liste des sauvegardes."""
        backup_listbox.delete(0, tk.END)
        result = get_backups_paginated(page=current_page, items_per_page=items_per_page)

        backup_results = result["backups"]

        # Ajouter une ligne d'en-tête
        backups.clear()
        header_text = f"{'ID':<5} {'Chemin de sauvegarde':<130} {'Date de création':<20}"
        backup_listbox.insert(tk.END, header_text)
        backup_listbox.itemconfig(0, bg="#D6EAF8", fg="#154360")

        for backup in backup_results:
            backup_text = f"{backup[0]:<5} {backup[1]:<100} {backup[2]}"
            backup_listbox.insert(tk.END, backup_text)
            backups.append(backup)

        pagination_label.config(
            text=f"Page {result['current_page']} sur {result['total_pages']}"
        )

    def perform_backup():
        user_directory = os.path.expanduser("~") 
        save_directory = os.path.join(user_directory, "Datas", "Factures") 
        os.makedirs(save_directory, exist_ok=True)
        base_file_name = "database_backup"
        extension = ".db"
        backup_file_name = f"{base_file_name}{extension}"
        backup_path = os.path.join(save_directory, backup_file_name)
        counter = 0
        while True:
            if counter == 0:
                backup_file_name = f"{base_file_name}{extension}" 
            else:
                backup_file_name = f"{base_file_name}_{counter}{extension}" 
            backup_path = os.path.join(save_directory, backup_file_name)

            if not os.path.exists(backup_path): 
                break
            counter += 1

        try:
            source_db_path = "database/database.db" 
            shutil.copyfile(source_db_path, backup_path)
            add_backup(backup_path)
            update_backup_listbox()
            messagebox.showinfo(
                "Succès",
                f"Sauvegarde effectuée avec succès dans :\n{backup_path}"
            )
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier source introuvable pour la sauvegarde.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {e}")

    def perform_restore():
        selected_index = backup_listbox.curselection()
        if selected_index and selected_index[0] > 0: 
            index = selected_index[0] - 1 
            backup = backups[index] 
            backup_details = get_backup_by_id(backup[0]) 
            if backup_details:
                try:
                    restore_path = backup_details[1] 
                    source_db_path = "database/database.db" 
                    shutil.copyfile(restore_path, source_db_path)
                    update_backup_listbox()
                    messagebox.showinfo(
                        "Succès",
                        f"La base de données a été restaurée avec succès depuis :\n{restore_path}"
                    )
                except FileNotFoundError:
                    messagebox.showerror(
                        "Erreur",
                        f"Fichier de sauvegarde introuvable :\n{restore_path}"
                    )
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la restauration : {e}")
            else:
                messagebox.showerror("Erreur", "Sauvegarde non trouvée.")
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner une sauvegarde.")

    def delete_selected_backup():
        """Supprime une sauvegarde sélectionnée."""
        selected_index = backup_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            backup_id = backups[selected_index[0] - 1][0]
            try:
                delete_backup(backup_id)
                update_backup_listbox()
                messagebox.showinfo("Succès", "Sauvegarde supprimée avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner une sauvegarde.")

    def next_page():
        """Passe à la page suivante."""
        nonlocal current_page
        result = get_backups_paginated(page=current_page + 1, items_per_page=items_per_page)
        if result["backups"]:
            current_page += 1
            update_backup_listbox()

    def previous_page():
        """Revient à la page précédente."""
        nonlocal current_page
        if current_page > 1:
            current_page -= 1
            update_backup_listbox()

    # Boutons principaux
    action_frame = tk.Frame(window, bg="#f7f7f7", pady=20)
    action_frame.pack(fill="x", padx=20)

    tk.Button(
        action_frame,
        text="Effectuer une Sauvegarde",
        command=perform_backup,
        bg="#2980B9",
        fg="white",
        font=("Arial", 16),
        width=25
    ).pack(side="left", padx=10)

    tk.Button(
        action_frame,
        text="Restaurer une Sauvegarde",
        command=perform_restore,
        bg="#27AE60",
        fg="white",
        font=("Arial", 16),
        width=25
    ).pack(side="left", padx=10)

    tk.Button(
        action_frame,
        text="Supprimer une Sauvegarde",
        command=delete_selected_backup,
        bg="#C0392B",
        fg="white",
        font=("Arial", 16),
        width=25
    ).pack(side="left", padx=10)

    # Liste des sauvegardes
    list_frame = tk.Frame(window, bg="#f7f7f7", pady=20)
    list_frame.pack(fill="both", expand=True, padx=20)

    backup_listbox = tk.Listbox(list_frame, font=("Arial", 14), height=15)
    backup_listbox.pack(fill="both", expand=True, pady=10)

    # Pagination
    pagination_frame = tk.Frame(window, bg="#f7f7f7")
    pagination_frame.pack(fill="x", pady=10)

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

    update_backup_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_backup_restore_window()
    root.mainloop()