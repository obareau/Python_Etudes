import re
import os
from tkinter import Tk, Label, Entry, Button, Text, filedialog, END, messagebox, OptionMenu, StringVar

class RegexTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Testeur d'Expressions Régulières")
        self.regex_examples = self.get_examples()
        self.init_widgets()

    def init_widgets(self):
        # Widgets principaux
        Label(self.root, text="Expression Régulière :").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.regex_entry = Entry(self.root, width=50)
        self.regex_entry.grid(row=0, column=1, padx=5, pady=5)
        Button(self.root, text="Analyser", command=self.analyze_regex).grid(row=0, column=2, padx=5, pady=5)

        # Menu déroulant pour les exemples
        Label(self.root, text="Exemples de Regex :").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.example_var = StringVar(self.root)
        self.example_var.set("Choisir un exemple")
        self.example_menu = OptionMenu(self.root, self.example_var, *self.regex_examples.keys(),
                                       command=lambda _: self.apply_example_regex())
        self.example_menu.grid(row=1, column=1, padx=5, pady=5)

        # Description de l'exemple
        Label(self.root, text="Description :").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.description_label = Text(self.root, width=60, height=5, state="disabled", wrap="word")
        self.description_label.grid(row=2, column=1, padx=5, pady=5)

        # Zone de texte pour analyser
        Label(self.root, text="Texte à Analyser :").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.text_input = Text(self.root, width=80, height=10)
        self.text_input.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # Résultats
        Label(self.root, text="Résultats :").grid(row=4, column=0, sticky="nw", padx=5, pady=5)
        self.result_output = Text(self.root, width=80, height=10, state="normal")
        self.result_output.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        # Boutons supplémentaires
        Button(self.root, text="Charger Fichier", command=self.load_file).grid(row=5, column=0, padx=5, pady=5)
        Button(self.root, text="Enregistrer Résultats", command=self.save_results).grid(row=5, column=2, padx=5, pady=5)

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
            "Numéro de sécurité sociale français": {
                "regex": r"^[1-2]\d{2}(0[1-9]|1[0-2])\d{2}\d{3}\d{3}\d{2}$",
                "description": "Valide un numéro de sécurité sociale français complet."
            },
            "Code postal français": {
                "regex": r"^\d{5}$",
                "description": "Valide un code postal français à 5 chiffres."
            },
            "Plaque d'immatriculation française": {
                "regex": r"^[A-Z]{2}-\d{3}-[A-Z]{2}$",
                "description": "Valide les plaques d'immatriculation françaises (format post-2009)."
            },
            "Numéro SIRET": {
                "regex": r"^\d{14}$",
                "description": "Valide un numéro SIRET (14 chiffres)."
            },
            "Numéro SIREN": {
                "regex": r"^\d{9}$",
                "description": "Valide un numéro SIREN (9 chiffres)."
            },
            "Validation d'un IBAN français": {
                "regex": r"^FR\d{2}\d{10}[A-Z0-9]{11,13}$",
                "description": "Valide un IBAN français."
            },
            "URL valide": {
                "regex": r"^https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:/[\w._~:/?#[\]@!$&'()*+,;=-]*)?$",
                "description": "Valide une URL (HTTP ou HTTPS)."
            },
            "Date au format JJ/MM/AAAA": {
                "regex": r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$",
                "description": "Valide une date au format français (jour/mois/année)."
            }
        }

    def apply_example_regex(self):
        selected_example = self.example_var.get()
        if selected_example in self.regex_examples:
            example = self.regex_examples[selected_example]
            self.regex_entry.delete(0, END)
            self.regex_entry.insert(END, example["regex"])
            self.description_label.config(state="normal")
            self.description_label.delete("1.0", END)
            self.description_label.insert(END, example["description"])
            self.description_label.config(state="disabled")

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier texte", filetypes=[("Fichiers texte", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_input.delete("1.0", END)
                    self.text_input.insert(END, content)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")

    def analyze_regex(self):
        regex = self.regex_entry.get()
        text = self.text_input.get("1.0", END).strip()
        if not regex or not text:
            messagebox.showwarning("Avertissement", "Veuillez entrer une regex et un texte.")
            return

        try:
            pattern = re.compile(regex)
            matches = list(pattern.finditer(text))
        except re.error as e:
            messagebox.showerror("Erreur", f"Erreur dans la regex : {e}")
            return

        self.result_output.delete("1.0", END)
        if matches:
            self.result_output.insert(END, f"Nombre de correspondances : {len(matches)}\n")
            self.result_output.insert(END, "Correspondances :\n")
            for match in matches:
                self.result_output.insert(END, f"- {match.group()} (Position {match.start()}-{match.end()})\n")
        else:
            self.result_output.insert(END, "Aucune correspondance trouvée.")

    def save_results(self):
        save_path = filedialog.asksaveasfilename(title="Enregistrer les résultats", defaultextension=".txt")
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as file:
                    file.write(self.result_output.get("1.0", END))
                messagebox.showinfo("Succès", f"Résultats enregistrés dans : {save_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder les résultats : {e}")

# Lancer l'application
if __name__ == "__main__":
    root = Tk()
    app = RegexTesterApp(root)
    root.mainloop()
