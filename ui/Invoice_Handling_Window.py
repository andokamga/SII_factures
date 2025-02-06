import tkinter as tk
from tkinter import messagebox
from invoices.invoices import *
from clients.clients import *
from products.products import *
import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
import os
from clients.clients import *
from products.products import *
from invoices.invoices import *
from tkinter import ttk, messagebox, Toplevel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os
import webbrowser
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox


def open_invoice_handling_window():
    invoice_window = tk.Toplevel()
    invoice_window.title("Gestion des Factures")

    screen_width = invoice_window.winfo_screenwidth()
    screen_height = invoice_window.winfo_screenheight()
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.9)
    invoice_window.geometry(f"{window_width}x{window_height}")
    invoice_window.state('zoomed')
    invoice_window.config(bg="#f7f7f7")

    title_frame = tk.Frame(invoice_window, bg="#f7f7f7", pady=10)
    title_frame.pack(fill="x", padx=20)
    title_label = tk.Label(
        title_frame,
        text="Gestion des Factures",
        font=("Arial", 26, "bold"),
        bg="#f7f7f7",
        fg="#2C3E50"
    )
    title_label.pack()

    # Champ de recherche
    search_frame = tk.Frame(invoice_window, bg="#f7f7f7", pady=5)
    search_frame.pack(fill="x", padx=20, pady=(10, 0))

    search_var = tk.StringVar()

    tk.Label(
        search_frame, text="Client ID :", bg="#f7f7f7", font=("Arial", 14)
    ).pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 14))
    search_entry.pack(side="left", padx=5)
    tk.Button(
        search_frame,
        text="Rechercher",
        command=lambda: search_invoices_by_id(),
        bg="#2980B9",
        fg="white",
        font=("Arial", 14),
    ).pack(side="left", padx=5)

    # Frame principale
    crud_frame = tk.Frame(invoice_window, bg="#f7f7f7", padx=20, pady=20)
    crud_frame.pack(fill="both", expand=True)

    items_per_page = 20
    current_page = 1
    invoice_database = []

    def update_invoice_listbox(invoices=None):
        """Met à jour la liste des factures dans la Listbox."""
        invoice_listbox.delete(0, tk.END)

        # En-tête
        header_text = "ID         Client ID        Client Nom        Client Téléphone        Tax (€)       Total (€)               Référence                            Date"
        invoice_listbox.insert(tk.END, header_text)
        invoice_listbox.itemconfig(0, bg="#D6EAF8", fg="#154360")

        if invoices is None:  # Si aucune facture n'est fournie, récupérer toutes les factures
            result = get_all_invoices(page=current_page, items_per_page=items_per_page)
            invoices = result["invoices"]

        invoice_database.clear()
        for invoice in invoices:
            client = get_client_by_id(invoice[1])
            invoice_database.append(invoice)
            invoice_text = f"{invoice[0]:<10}  {invoice[1]:<20}   {client[1]:<25}  {client[3]:<20}   {invoice[3]:<10.2f} {invoice[2]:<15.2f}  {invoice[4]:<30} {invoice[5]}"
            invoice_listbox.insert(tk.END, invoice_text)
        update_pagination_label(result["current_page"], result["total_pages"])

    def search_invoices_by_id():
        """Rechercher les factures par numéro de téléphone."""
        id = search_var.get().strip()
        if id:
            result = get_invoices_by_id(id, page=current_page, items_per_page=items_per_page)
            invoices = result["invoices"]
            if invoices:
                update_invoice_listbox(invoices)
            else:
                messagebox.showinfo("Information", "Aucune facture trouvée pour ce numéro de téléphone.")
        else:
            update_invoice_listbox()

    def update_pagination_label(current_page, total_pages):
        pagination_label.config(text=f"Page {current_page} sur {total_pages}")

    def next_page():
        nonlocal current_page
        result = get_all_invoices(page=current_page, items_per_page=items_per_page)
        if current_page < result["total_pages"]:
            current_page += 1
            update_invoice_listbox()

    def previous_page():
        nonlocal current_page
        if current_page > 1:
            current_page -= 1
            update_invoice_listbox()

    def delete_invoice_ui():
        selected_index = invoice_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0] - 1
            invoice = invoice_database[index]
            confirm = messagebox.askyesno("Confirmation", f"Supprimer la facture ID {invoice[0]} ?")
            if confirm:
                delete_invoice(invoice[0])
                update_invoice_listbox()
                messagebox.showinfo("Succès", "Facture supprimée avec succès.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture à supprimer.")

    def print_invoice_ui():
        selected_index = invoice_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0] - 1
            invoice = invoice_database[index]
            open_and_print_pdf(generate_pdf(invoice))
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture à imprimer.")

    def generate_pdf(invoice):
        selected_index = invoice_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0] - 1
            invoice = invoice_database[index]
            client = get_client_by_id(invoice[1])
            invoice_details,items = get_invoice_with_items(invoice[0])
            user_directory = os.path.expanduser("~") 
            save_directory = os.path.join(user_directory, "Documents", "Factures") 
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            filename = os.path.join(save_directory, f"Facture_{invoice[4]}.pdf")
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, f"Facture ID: {invoice[4]}")
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 80, f"Client: {client[1]} ({client[3]})")
            c.drawString(50, height - 100, f"Téléphone: {client[3]}")
            c.drawString(50, height - 120, f"Date de la facture : {invoice[5]}")
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 150, "Détail de la facture")
            y = height - 180
            table_data = [["Article", "Quantité", "Prix Unitaire (€)", "Total (€)"]] 
            for item in items:
                produit = get_product_by_id(item[2])
                table_data.append([produit[1], item[3], f"{produit[3]}", f"{item[4]:.2f}"])
            table_data.append(["", "", "Taxe:", f"{invoice[3]:.2f}"])
            table_data.append(["", "", "Total:", f"{invoice[2]:.2f}"])
            table = Table(table_data, colWidths=[200, 100, 150, 100])
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey), 
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), 
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'), 
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), 
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12), 
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            table.setStyle(style)
            table.wrapOn(c, width, height)
            table.drawOn(c, 50, y - len(table_data) * 20) 
            signature_y = y - (len(table_data) + 3) * 20
            c.setFont("Helvetica", 12)
            c.drawString(50, signature_y, "Signature du client :")
            c.line(200, signature_y, 400, signature_y) 

            c.drawString(50, signature_y - 40, "Signature du vendeur :")
            c.line(200, signature_y - 40, 400, signature_y - 40) 
            c.save()
            return filename
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture à imprimer.")

    def open_and_print_pdf(filepath):
        try:
            if os.name == "nt": 
                os.startfile(filepath)
            else:  
                webbrowser.open(filepath)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")

    def view_invoice_details():
        selected_index = invoice_listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0] - 1
            invoice = invoice_database[index]
            client = get_client_by_id(invoice[1])
            invoice_details,items = get_invoice_with_items(invoice[0])
            detail_window = tk.Toplevel(invoice_window)
            detail_window.title(f"Détails de la Facture {invoice[0]}")
            detail_text = tk.Text(detail_window, font=("Arial", 12))
            detail_text.pack(fill="both", expand=True)
            detail_text.insert("end", f"Client ID: {invoice[1]}\n")
            detail_text.insert("end", f"Client Nom: {client[1]}\n")
            detail_text.insert("end", f"Client Téléphone: {client[3]}\n")
            detail_text.insert("end", f"Tax: {invoice[3]:.2f} €\n")
            detail_text.insert("end", f"Total: {invoice[2]:.2f} €\n")
            detail_text.insert("end", f"Référence: {invoice[4]}\n")
            detail_text.insert("end", f"Date: {invoice[5]}\n\n")
            detail_text.insert("end", "=== Articles de la facture ===\n")
            if items:
                for item in items:
                    produit = get_product_by_id(item[2])
                    detail_text.insert("end", f"Produit ID: {item[2]}, Nom: {produit[1]}, Quantité: {item[3]}, Prix: {item[4]:.2f} €\n")
            else:
                detail_text.insert("end", "Aucun article trouvé pour cette facture.\n")
            detail_text.config(state="disabled")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une facture à afficher.")

    button_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tk.Button(
        button_frame,
        text="Supprimer",
        command=delete_invoice_ui,
        bg="#C0392B",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=0, padx=5)
    tk.Button(
        button_frame,
        text="Imprimer",
        command=print_invoice_ui,
        bg="#27AE60",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=1, padx=5)
    tk.Button(
        button_frame,
        text="Détails",
        command=view_invoice_details,
        bg="#2980B9",
        fg="white",
        font=("Arial", 14),
        width=15,
    ).grid(row=0, column=2, padx=5)

    invoice_listbox = tk.Listbox(crud_frame, font=("Arial", 14), height=15)
    invoice_listbox.grid(row=1, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

    pagination_frame = tk.Frame(crud_frame, bg="#f7f7f7")
    pagination_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

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
    crud_frame.rowconfigure(1, weight=1)

    update_invoice_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_invoice_handling_window()
    root.mainloop()