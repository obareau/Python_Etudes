#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import math


# Fonction pour calculer les volumes nécessaires
def calculer():
    try:
        # Récupérer la concentration de la base de nicotine choisie (10 ou 20 mg/mL)
        C_nicotine = nicotine_var.get()
        C_final = float(entry_C_final.get())
        V_total = float(entry_V_total.get())
        pourcentage_arome = float(entry_pourcentage_arome.get())

        # Calcul du volume de nicotine nécessaire (V_nicotine)
        V_nicotine = (C_final * V_total) / C_nicotine

        # Calcul du nombre de flacons nécessaires (un flacon fait 10 mL)
        nombre_flacons_nicotine = math.ceil(V_nicotine / 10)

        # Calcul du volume d'arôme nécessaire (V_arome)
        V_arome = (pourcentage_arome / 100) * V_total

        # Calcul du volume de la base PG/VG nécessaire (V_base)
        V_base = V_total - V_nicotine - V_arome

        # Affichage des résultats dans une boîte de dialogue
        result_message = (
            f"Volume de base de nicotine à ajouter : {V_nicotine:.2f} mL\n"
            f"Nombre de flacons de nicotine nécessaires (10 mL chacun) : {nombre_flacons_nicotine} flacons\n"
            f"Volume d'arôme à ajouter : {V_arome:.2f} mL\n"
            f"Volume de base PG/VG à ajouter : {V_base:.2f} mL"
        )
        messagebox.showinfo("Résultats du Calcul", result_message)

    except ValueError:
        messagebox.showerror(
            "Erreur", "Veuillez entrer des valeurs numériques valides."
        )


# Création de la fenêtre principale
root = tk.Tk()
root.title("Calculateur de E-Liquide")

# Labels et champs de saisie
tk.Label(root, text="Concentration de nicotine finale souhaitée (mg/mL) :").grid(
    row=0, column=0, padx=10, pady=5
)
entry_C_final = tk.Entry(root)
entry_C_final.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Volume total du e-liquide final (mL) :").grid(
    row=1, column=0, padx=10, pady=5
)
entry_V_total = tk.Entry(root)
entry_V_total.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Pourcentage d'arôme (%) :").grid(row=2, column=0, padx=10, pady=5)
entry_pourcentage_arome = tk.Entry(root)
entry_pourcentage_arome.grid(row=2, column=1, padx=10, pady=5)

# Choix de la concentration de nicotine (10 ou 20 mg/mL)
tk.Label(root, text="Choisissez la concentration de la base de nicotine :").grid(
    row=3, column=0, columnspan=2, padx=10, pady=5
)

nicotine_var = tk.IntVar(value=20)  # Valeur par défaut de 20 mg/mL
radio_10 = tk.Radiobutton(root, text="10 mg/mL", variable=nicotine_var, value=10)
radio_20 = tk.Radiobutton(root, text="20 mg/mL", variable=nicotine_var, value=20)

radio_10.grid(row=4, column=0, padx=10, pady=5)
radio_20.grid(row=4, column=1, padx=10, pady=5)

# Bouton pour lancer le calcul
button_calculer = tk.Button(root, text="Calculer", command=calculer)
button_calculer.grid(row=5, column=0, columnspan=2, pady=10)

# Lancement de la boucle principale
root.mainloop()
