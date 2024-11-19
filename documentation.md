
# Documentation: Utilisation du Calculateur de E-Liquide

## Introduction

Ce programme est conçu pour les créateurs de e-liquides DIY. Il permet de calculer les proportions exactes de base, booster, et arômes nécessaires pour créer un e-liquide personnalisé avec des fonctionnalités avancées telles que la gestion des stocks, la sauvegarde des recettes, et la génération d'étiquettes.

---

## Fonctionnalités Principales

1. **Calculateur** : Calcule automatiquement les proportions de PG/VG, nicotine et arômes.
2. **Gestion des Arômes** : Ajoutez des arômes personnalisés avec leurs types, proportions, PG/VG et marques.
3. **Sauvegarde et Chargement** : Enregistrez vos recettes en JSON et rechargez-les facilement.
4. **Génération d'Étiquettes** : Créez des étiquettes imprimables avec QR Code et informations complètes.
5. **Visualisation Graphique** : Affichez les proportions PG/VG, nicotine et arômes sous forme de graphiques.
6. **Gestion des Stocks** : Suivez vos stocks de base, booster, et arômes, avec alertes pour les quantités insuffisantes.
7. **Modes Débutant et Avancé** : Choisissez un mode adapté à votre niveau d'expertise.

---

## Installation

### Prérequis
- Python 3.8 ou version supérieure
- Dépendances (installables via `requirements.txt`)

### Installation
1. Clonez le dépôt GitHub :
   ```bash
   git clone https://github.com/your-username/eliquid-calculator.git
   cd eliquid-calculator
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancez l'application :
   ```bash
   python eliquid_calculator.py
   ```

---

## Utilisation

### Interface Principale

1. **Base** :
   - Définissez les proportions de PG/VG pour la base.
   - Indiquez si la base est nicotinée et entrez le taux de nicotine, le cas échéant.
   - Sélectionnez ou entrez la marque de la base.

2. **Booster** :
   - Indiquez le taux de nicotine du booster ainsi que les proportions PG/VG.
   - Sélectionnez ou entrez la marque du booster.

3. **Arômes** :
   - Ajoutez vos arômes avec leurs noms, types, proportions, PG/VG et marques.
   - Le temps de steep est automatiquement calculé en fonction du type d’arôme.

4. **Volume Total** :
   - Entrez le volume total souhaité pour votre e-liquide.

5. **Calcul** :
   - Cliquez sur le bouton "Calculer" pour obtenir les proportions exactes des ingrédients.

---

### Gestion des Arômes

1. **Ajouter un Arôme** :
   - Cliquez sur "Ajouter Arôme".
   - Remplissez les champs pour le nom, le type, la proportion, les proportions PG/VG, et la marque.
   - Cliquez sur "Ajouter" pour sauvegarder l’arôme dans la recette.

2. **Liste des Arômes** :
   - Tous les arômes ajoutés apparaissent dans la liste avec leurs détails (nom, type, proportions, temps de steep).

---

### Sauvegarde et Chargement

1. **Sauvegarder une Recette** :
   - Cliquez sur "Sauvegarder Recette".
   - Sélectionnez l’emplacement et entrez un nom de fichier pour sauvegarder les données au format JSON.

2. **Charger une Recette** :
   - Cliquez sur "Charger Recette".
   - Sélectionnez un fichier JSON précédemment sauvegardé pour recharger la recette.

---

### Génération d'Étiquettes

1. Cliquez sur "Générer Étiquette".
2. Une fenêtre s’ouvre avec :
   - Les proportions de PG/VG, nicotine, et arômes.
   - Le temps de steep recommandé.
   - Un QR Code contenant toutes les informations de la recette.
3. Vous pouvez imprimer directement cette étiquette ou l’enregistrer.

---

### Visualisation Graphique

1. Cliquez sur "Graphique".
2. Une fenêtre s’ouvre avec un graphique interactif montrant :
   - La répartition des proportions PG/VG, nicotine, et arômes.
   - Vous pouvez comparer les graphiques entre plusieurs recettes.

---

### Gestion des Stocks

1. Les stocks de base, booster et arômes sont suivis automatiquement.
2. Lorsqu’un calcul est effectué, les quantités correspondantes sont déduites des stocks.
3. Si une quantité est insuffisante, une alerte est affichée.

---

## Fonctionnalités Avancées

1. **Mode Débutant et Avancé** :
   - Débutant : Champs simplifiés (PG/VG, nicotine, arômes de base).
   - Avancé : Accès complet (marques, gestion fine des proportions, etc.).

2. **Comparaison de Recettes** :
   - Chargez deux recettes JSON.
   - Comparez leurs proportions PG/VG, nicotine, et arômes côte à côte.

3. **Historique** :
   - Les dernières recettes calculées sont enregistrées dans un historique consultable.

---

## Conseils pour les Recettes

1. **Temps de Steep** :
   - Respectez le temps de steep recommandé pour chaque type d’arôme (fruité, gourmand, mentholé, etc.).
   - Consultez la liste dans la section "Gestion des Arômes".

2. **Étiquetage** :
   - Ajoutez un QR Code pour un accès rapide aux informations de votre e-liquide.
   - Notez la date de création sur l'étiquette.

3. **Optimisation des Stocks** :
   - Surveillez régulièrement vos quantités disponibles pour éviter les ruptures.
   - Utilisez les alertes de stock pour planifier vos achats.

---

## Dépannage

### Problèmes Courants

1. **Proportions Invalides** :
   - Assurez-vous que PG + VG = 100%.
   - Vérifiez que le total des proportions d’arômes ne dépasse pas 100%.

2. **JSON Non Chargé** :
   - Vérifiez que le fichier est au format JSON valide.
   - Rechargez une recette précédemment sauvegardée par le programme.

---

## Technologies Utilisées

- **Python** : Langage principal.
- **Tkinter** : Interface utilisateur.
- **Matplotlib** : Graphiques.
- **qrcode** : Génération des QR Codes.
- **Pillow** : Gestion des images pour les QR Codes.

---

## Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d'informations.

---

## Contribution

Les contributions sont les bienvenues ! Forkez le dépôt, créez une branche, et proposez vos modifications via une pull request.

---

## Contact

Pour toute question ou suggestion, contactez-nous à [olivier.bareau@gmail.com].
