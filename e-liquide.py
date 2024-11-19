'''
Calculateur de E-Liquide version 1.0'''

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import matplotlib.pyplot as plt
from math import ceil
from datetime import datetime
import qrcode
from io import BytesIO
from PIL import Image, ImageTk


class EliquidCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculateur de E-Liquide")
        self.aromes = []
        self.stocks = {
            "base": {"quantity": 1000, "marque": "Default Base"},
            "booster": {"quantity": 500, "marque": "Default Booster"},
            "aromes": {}
        }
        self.recipes_history = []
        self.mode = tk.StringVar(value="Avancé")  # Mode par défaut : Avancé

        # Variables
        self.base_nicotined = tk.BooleanVar()
        self.base_pg = tk.IntVar(value=50)
        self.base_vg = tk.IntVar(value=50)
        self.base_nicotine = tk.DoubleVar(value=3)
        self.base_marque = tk.StringVar(value="Marque Base")

        self.booster_nicotine = tk.DoubleVar(value=20)
        self.booster_pg = tk.IntVar(value=50)
        self.booster_vg = tk.IntVar(value=50)
        self.booster_volume = tk.DoubleVar(value=10)
        self.booster_marque = tk.StringVar(value="Marque Booster")

        self.total_volume = tk.DoubleVar(value=100)
        self.cost_base = tk.DoubleVar(value=0)
        self.cost_booster = tk.DoubleVar(value=0)
        self.cost_aromes = tk.DoubleVar(value=0)

        self.create_widgets()

    def create_widgets(self):
        # Section Mode
        ttk.Label(self.root, text="Mode :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Combobox(self.root, textvariable=self.mode, values=["Débutant", "Avancé"], state="readonly").grid(row=0, column=1, padx=10, pady=5)

        # Section Base
        ttk.Label(self.root, text="Base :").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(self.root, text="PG (%)").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.base_pg, width=5).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="VG (%)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.base_vg, width=5).grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(self.root, text="Marque :").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.base_marque, width=20).grid(row=4, column=1, padx=5, pady=5)

        ttk.Checkbutton(self.root, text="Base Nicotinée", variable=self.base_nicotined, command=self.toggle_base_nicotine).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(self.root, text="Taux de Nicotine (mg/ml)").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.base_nicotine_entry = ttk.Entry(self.root, textvariable=self.base_nicotine, width=5, state="disabled")
        self.base_nicotine_entry.grid(row=6, column=1, padx=5, pady=5)

        # Section Booster
        ttk.Label(self.root, text="Booster :").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        ttk.Label(self.root, text="Nicotine (mg/ml)").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.booster_nicotine, width=5).grid(row=2, column=3, padx=5, pady=5)
        ttk.Label(self.root, text="PG (%)").grid(row=3, column=2, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.booster_pg, width=5).grid(row=3, column=3, padx=5, pady=5)
        ttk.Label(self.root, text="VG (%)").grid(row=4, column=2, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.booster_vg, width=5).grid(row=4, column=3, padx=5, pady=5)
        ttk.Label(self.root, text="Marque :").grid(row=5, column=2, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.booster_marque, width=20).grid(row=5, column=3, padx=5, pady=5)

        # Section Arômes
        ttk.Label(self.root, text="Arômes :").grid(row=7, column=0, padx=10, pady=5, sticky="w")
        ttk.Button(self.root, text="Ajouter Arôme", command=self.add_arome).grid(row=7, column=1, padx=5, pady=5)
        self.aromes_list = tk.Text(self.root, width=40, height=5, state="disabled")
        self.aromes_list.grid(row=8, column=0, columnspan=4, padx=10, pady=5)

        # Section Calcul
        ttk.Label(self.root, text="Volume Total (ml)").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.total_volume, width=5).grid(row=9, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Calculer", command=self.calculate).grid(row=10, column=0, columnspan=2, padx=5, pady=10)
        ttk.Button(self.root, text="Graphique", command=self.show_graph).grid(row=10, column=2, columnspan=2, padx=5, pady=10)
        ttk.Button(self.root, text="Sauvegarder Recette", command=self.save_recipe).grid(row=11, column=0, columnspan=2, padx=5, pady=10)
        ttk.Button(self.root, text="Générer Étiquette", command=self.generate_label).grid(row=11, column=2, columnspan=2, padx=5, pady=10)

    def toggle_base_nicotine(self):
        """Active ou désactive l'entrée pour la nicotine de la base."""
        if self.base_nicotined.get():
            self.base_nicotine_entry.config(state="normal")
        else:
            self.base_nicotine_entry.config(state="disabled")
            self.base_nicotine.set(0)

    def add_arome(self):
        """Ajoute un arôme à la liste avec ses détails."""
        new_window = tk.Toplevel(self.root)
        new_window.title("Ajouter Arôme")
        ttk.Label(new_window, text="Nom de l'Arôme :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(new_window, text="Type").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(new_window, text="Proportion (%)").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(new_window, text="PG (%)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(new_window, text="VG (%)").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(new_window, text="Marque :").grid(row=5, column=0, padx=10, pady=5, sticky="w")

        ar_name = tk.StringVar()
        ar_type = tk.StringVar(value="fruité")
        ar_proportion = tk.DoubleVar(value=10)
        ar_pg = tk.IntVar(value=100)
        ar_vg = tk.IntVar(value=0)
        ar_marque = tk.StringVar(value="Marque Arôme")

        ttk.Entry(new_window, textvariable=ar_name).grid(row=0, column=1, padx=5, pady=5)
        ttk.Combobox(new_window, textvariable=ar_type, values=["frais", "fruité", "mentholé", "classic", "gourmand",
                                                              "fruité frais", "classic frais", "gourmand frais", "autre"]).grid(row=1, column=1, padx=5, pady=5)
        ttk.Entry(new_window, textvariable=ar_proportion).grid(row=2, column=1, padx=5, pady=5)
        ttk.Entry(new_window, textvariable=ar_pg).grid(row=3, column=1, padx=5, pady=5)
        ttk.Entry(new_window, textvariable=ar_vg).grid(row=4, column=1, padx=5, pady=5)
        ttk.Entry(new_window, textvariable=ar_marque).grid(row=5, column=1, padx=5, pady=5)

        def save_arome():
            if ar_name.get() and ar_proportion.get() > 0:
                self.aromes.append({"nom": ar_name.get(),
                                    "type": ar_type.get(),
                                    "proportion": ar_proportion.get(),
                                    "pg": ar_pg.get(),
                                    "vg": ar_vg.get(),
                                    "marque": ar_marque.get()})
                self.update_aromes_list()
                new_window.destroy()
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement.")

        ttk.Button(new_window, text="Ajouter", command=save_arome).grid(row=6, column=0, columnspan=2, pady=10)

    def update_aromes_list(self):
        """Met à jour la liste affichée des arômes."""
        self.aromes_list.config(state="normal")
        self.aromes_list.delete("1.0", tk.END)
        for ar in self.aromes:
            steep_time = self.get_steep_time(ar["type"])
            self.aromes_list.insert(tk.END, f"{ar['nom']} ({ar['type']}) - {ar['proportion']}% (PG {ar['pg']} / VG {ar['vg']})\n"
                                            f"Marque : {ar['marque']} - Temps de maturation : {steep_time} jours\n")
        self.aromes_list.config(state="disabled")

    def save_recipe(self):
        """Sauvegarde la recette actuelle dans un fichier JSON."""
        recipe = {
            "date_creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "base": {
                "pg": self.base_pg.get(),
                "vg": self.base_vg.get(),
                "nicotine": self.base_nicotine.get(),
                "marque": self.base_marque.get(),
            },
            "booster": {
                "nicotine": self.booster_nicotine.get(),
                "pg": self.booster_pg.get(),
                "vg": self.booster_vg.get(),
                "volume": self.booster_volume.get(),
                "marque": self.booster_marque.get(),
            },
            "aromes": self.aromes,
            "total_volume": self.total_volume.get(),
            "steep_time": self.calculate_steep_time()
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(recipe, f, indent=4)
            messagebox.showinfo("Succès", "Recette sauvegardée avec succès !")

    def generate_label(self):
        """Génère une étiquette pour la recette actuelle."""
        steep_time = self.calculate_steep_time()
        label_text = (
            f"Recette créée le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"- PG/VG : {self.base_pg.get()}% / {self.base_vg.get()}%\n"
            f"- Nicotine : {self.base_nicotine.get()} mg/ml\n"
            f"- Marque Base : {self.base_marque.get()}\n"
            f"- Volume Total : {self.total_volume.get()} ml\n"
            f"- Booster (Marque : {self.booster_marque.get()}): {self.booster_nicotine.get()} mg/ml\n"
            f"- Arômes :\n"
        )
        for ar in self.aromes:
            label_text += f"  - {ar['nom']} ({ar['type']}) : {ar['proportion']}% (PG {ar['pg']}/VG {ar['vg']})\n"
            label_text += f"    Marque : {ar['marque']}\n"

        label_text += f"Temps de maturation recommandé : {steep_time} jours"

        # Générer un QR Code pour la recette
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(label_text)
        qr.make(fit=True)
        qr_img = qr.make_image(fill="black", back_color="white")
        img_buffer = BytesIO()
        qr_img.save(img_buffer, format="PNG")
        qr_img_tk = ImageTk.PhotoImage(Image.open(img_buffer))

        # Afficher l'étiquette dans une fenêtre
        label_window = tk.Toplevel(self.root)
        label_window.title("Étiquette")
        text_widget = tk.Text(label_window, width=50, height=20)
        text_widget.insert("1.0", label_text)
        text_widget.config(state="disabled")
        text_widget.pack(padx=10, pady=10)

        qr_label = tk.Label(label_window, image=qr_img_tk)
        qr_label.image = qr_img_tk
        qr_label.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = EliquidCalculator(root)
    root.mainloop()

