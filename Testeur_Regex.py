import re
import os
import json
import csv
from tkinter import Tk, Label, Entry, Button, Text, filedialog, END, messagebox, OptionMenu, StringVar, ttk, Scrollbar

class RegexTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Testeur d'Expressions Régulières")
        self.regex_history = []
        self.mode_sombre = False

        # Widgets principaux
        self.init_widgets()

    def init_widgets(self):
        # Regex et menu d'exemples
        Label(self.root, text="Expression Régulière :").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.regex_entry = Entry(self.root, width=50)
        self.regex_entry.grid(row=0, column=1, padx=5, pady=5)
        self.regex_entry.bind("<KeyRelease>", lambda _: self.live_preview())

        # Exemples prédéfinis
        self.example_var = StringVar(self.root)
        self.example_var.set("Choisir un exemple")
        self.example_menu = OptionMenu(self.root, self.example_var, *self.get_examples().keys(), command=lambda _: self.apply_example_regex())
        self.example_menu.grid(row=0, column=2, padx=5, pady=5)

        # Zone de texte
        Label(self.root, text="Texte à Analyser :").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.text_input = Text(self.root, width=80, height=10)
        self.text_input.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.text_input.bind("<KeyRelease>", lambda _: self.live_preview())

        # Résultats
        Label(self.root, text="Résultats :").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.result_output = Text(self.root, width=80, height=10, state="normal")
        self.result_output.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        # Boutons supplémentaires
        Button(self.root, text="Charger Fichier", command=self.load_file).grid(row=3, column=0, padx=5, pady=5)
        Button(self.root, text="Analyser", command=self.analyze_regex).grid(row=3, column=1, padx=5, pady=5)
        Button(self.root, text="Enregistrer Résultats", command=self.save_results).grid(row=3, column=2, padx=5, pady=5)
        Button(self.root, text="Mode Sombre", command=self.toggle_mode_sombre).grid(row=4, column=2, padx=5, pady=5)

    def get_examples(self):
        return {
            "Validation d'un e-mail": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "Numéro de sécurité sociale français": r"^[1-2]\d{2}(0[1-9]|1[0-2])\d{2}\d{3}\d{3}\d{2}$",
            "Validation d'un IBAN": r"^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$",
            "Numéro de téléphone français": r"^0[1-9](\d{2}){4}$",
            "Code postal français": r"^\d{5}$"
        }

    def apply_example_regex(self):
        examples = self.get_examples()
        selected_example = self.example_var.get()
        if selected_example in examples:
            self.regex_entry.delete(0, END)
            self.regex_entry.insert(END, examples[selected_example])

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier", filetypes=[("Tous les fichiers", "*.*")])
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
            messagebox.showwarning("Avertissement", "Veuillez remplir la regex et le texte à analyser.")
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

        # Mise à jour de l'historique
        if regex not in self.regex_history:
            self.regex_history.append(regex)

    def live_preview(self):
        self.analyze_regex()

    def save_results(self):
        save_path = filedialog.asksaveasfilename(title="Enregistrer les résultats", defaultextension=".txt")
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as file:
                    file.write(self.result_output.get("1.0", END))
                messagebox.showinfo("Succès", f"Résultats enregistrés dans : {save_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder les résultats : {e}")

    def toggle_mode_sombre(self):
        if self.mode_sombre:
            self.root.config(bg="SystemButtonFace")
            self.mode_sombre = False
        else:
            self.root.config(bg="#2C2C2C")
            self.mode_sombre = True


# Lancer l'application
if __name__ == "__main__":
    root = Tk()
    app = RegexTesterApp(root)
    root.mainloop()
