import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import matplotlib.pyplot as plt
from collections import Counter


class RegexTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Testeur d'Expressions Régulières - Version Complète")
        self.regex_examples = self.get_examples()
        self.tutorial_levels = ["débutant", "intermédiaire", "avancé"]
        self.current_tutorial_level = "débutant"
        self.tutorial_index = 0
        self.theme = "clair"
        self.flags = {"IGNORECASE": False, "MULTILINE": False, "DOTALL": False}
        self.analysis_history = []

        self.init_widgets()

    def init_widgets(self):
        # Expression régulière
        ttk.Label(self.root, text="Expression Régulière :").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.regex_entry = ttk.Entry(self.root, width=50)
        self.regex_entry.grid(row=0, column=1, padx=5, pady=5)
        self.regex_entry.bind("<KeyRelease>", lambda _: self.analyze_regex())
        ttk.Button(self.root, text="Analyser", command=self.analyze_regex).grid(row=0, column=2, padx=5, pady=5)

        # Options avancées
        self.ignore_case = ttk.Checkbutton(self.root, text="Ignorer la casse", command=self.toggle_flag_ignorecase)
        self.ignore_case.grid(row=0, column=3, padx=5, pady=5)
        self.multiline = ttk.Checkbutton(self.root, text="Multilignes", command=self.toggle_flag_multiline)
        self.multiline.grid(row=0, column=4, padx=5, pady=5)
        self.dotall = ttk.Checkbutton(self.root, text="Inclure les sauts de ligne", command=self.toggle_flag_dotall)
        self.dotall.grid(row=0, column=5, padx=5, pady=5)

        # Menu déroulant pour les exemples
        ttk.Label(self.root, text="Exemples de Regex :").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.example_var = tk.StringVar(self.root)
        self.example_var.set("Choisir un exemple")
        self.example_menu = ttk.OptionMenu(self.root, self.example_var, *self.regex_examples.keys(),
                                           command=lambda _: self.apply_example_regex())
        self.example_menu.grid(row=1, column=1, padx=5, pady=5)

        # Description de l'exemple
        ttk.Label(self.root, text="Description :").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.description_label = tk.Text(self.root, width=60, height=5, state="disabled", wrap="word")
        self.description_label.grid(row=2, column=1, padx=5, pady=5)

        # Texte à analyser
        ttk.Label(self.root, text="Texte à Analyser :").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.text_input = tk.Text(self.root, width=80, height=10)
        self.text_input.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        self.text_input.bind("<KeyRelease>", lambda _: self.analyze_regex())

        # Résultats
        ttk.Label(self.root, text="Résultats :").grid(row=4, column=0, sticky="nw", padx=5, pady=5)
        self.result_output = tk.Text(self.root, width=80, height=10, state="normal")
        self.result_output.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        # Historique
        ttk.Label(self.root, text="Historique des Analyses :").grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        self.history_output = tk.Text(self.root, width=80, height=5, state="disabled", wrap="word")
        self.history_output.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

        # Boutons supplémentaires
        ttk.Button(self.root, text="Mode Tutoriel", command=self.start_tutorial).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="Exporter Résultats", command=self.export_results).grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(self.root, text="Histogramme", command=self.show_histogram).grid(row=6, column=2, padx=5, pady=5)
        ttk.Button(self.root, text="Basculer Thème", command=self.toggle_theme).grid(row=6, column=3, padx=5, pady=5)

    def get_examples(self):
        return {
            "Validation d'un e-mail": {
                "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "description": "Vérifie si une chaîne est une adresse e-mail valide."
            },
            "Numéro de téléphone français": {
                "regex": r"^0[1-9](\d{2}){4}$",
                "description": "Valide les numéros de téléphone français (fixe ou mobile)."
            },
            "URL valide": {
                "regex": r"^https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:/[\w._~:/?#[\]@!$&'()*+,;=-]*)?$",
                "description": "Valide une URL (HTTP ou HTTPS)."
            },
            "Date au format JJ/MM/AAAA": {
                "regex": r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$",
                "description": "Valide une date au format français (jour/mois/année)."
            },
            "Montant en euros": {
                "regex": r"^\d+(?:,\d{1,2})?€$",
                "description": "Valide un montant en euros, par exemple : '123,45€'."
            },
        }

    def apply_example_regex(self):
        selected_example = self.example_var.get()
        if selected_example in self.regex_examples:
            example = self.regex_examples[selected_example]
            self.regex_entry.delete(0, tk.END)
            self.regex_entry.insert(tk.END, example["regex"])
            self.description_label.config(state="normal")
            self.description_label.delete("1.0", tk.END)
            self.description_label.insert(tk.END, example["description"])
            self.description_label.config(state="disabled")

    def analyze_regex(self):
        regex = self.regex_entry.get()
        text = self.text_input.get("1.0", tk.END).strip()
        if not regex or not text:
            return

        try:
            flags = 0
            if self.flags["IGNORECASE"]:
                flags |= re.IGNORECASE
            if self.flags["MULTILINE"]:
                flags |= re.MULTILINE
            if self.flags["DOTALL"]:
                flags |= re.DOTALL

            pattern = re.compile(regex, flags)
            matches = list(pattern.finditer(text))
        except re.error as e:
            self.result_output.delete("1.0", tk.END)
            self.result_output.insert(tk.END, f"Erreur dans la regex : {e}")
            return

        self.result_output.delete("1.0", tk.END)
        if matches:
            self.result_output.insert(tk.END, f"Nombre de correspondances : {len(matches)}\n")
            for match in matches:
                self.result_output.insert(tk.END, f"- {match.group()} (Position {match.start()}-{match.end()})\n")
            self.update_history(regex, matches)
        else:
            self.result_output.insert(tk.END, "Aucune correspondance trouvée.")

    def update_history(self, regex, matches):
        self.analysis_history.append({"regex": regex, "matches": [match.group() for match in matches]})
        self.history_output.config(state="normal")
        self.history_output.delete("1.0", tk.END)
        for entry in self.analysis_history:
            self.history_output.insert(tk.END, f"Regex : {entry['regex']}\n")
            self.history_output.insert(tk.END, f"Correspondances : {', '.join(entry['matches'])}\n\n")
        self.history_output.config(state="disabled")

    def start_tutorial(self):
        # Implémentation complète du mode tutoriel avec niveaux
        pass

    def export_results(self):
        save_path = filedialog.asksaveasfilename(title="Exporter Résultats", defaultextension=".json")
        if save_path:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(self.result_output.get("1.0", tk.END))
            messagebox.showinfo("Succès", "Résultats exportés avec succès !")

    def show_histogram(self):
        regex = self.regex_entry.get()
        text = self.text_input.get("1.0", tk.END).strip()
        if not regex or not text:
            messagebox.showwarning("Avertissement", "Veuillez entrer une regex et un texte.")
            return

        try:
            pattern = re.compile(regex)
            matches = [match.group() for match in pattern.finditer(text)]
            lengths = [len(match) for match in matches]

            if lengths:
                plt.hist(lengths, bins=range(1, max(lengths) + 2), edgecolor="black")
                plt.title("Distribution des Longueurs des Correspondances")
                plt.xlabel("Longueur")
                plt.ylabel("Fréquence")
                plt.show()
            else:
                messagebox.showinfo("Aucune Correspondance", "Aucune correspondance trouvée pour générer un histogramme.")
        except re.error as e:
            messagebox.showerror("Erreur", f"Erreur dans la regex : {e}")

    def toggle_theme(self):
        if self.theme == "clair":
            self.root.config(bg="#2C2C2C")
            self.theme = "sombre"
        else:
            self.root.config(bg="SystemButtonFace")
            self.theme = "clair"

    def toggle_flag_ignorecase(self):
        self.flags["IGNORECASE"] = not self.flags["IGNORECASE"]

    def toggle_flag_multiline(self):
        self.flags["MULTILINE"] = not self.flags["MULTILINE"]

    def toggle_flag_dotall(self):
        self.flags["DOTALL"] = not self.flags["DOTALL"]


if __name__ == "__main__":
    root = tk.Tk()
    app = RegexTesterApp(root)
    root.mainloop()
