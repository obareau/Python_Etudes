'''
Programme qui permet de savoir si un nombre est pair ou impair'''
# Demande à l'utilisateur d'entrer un nombre
nombre = int(input("Entrez un nombre : "))

# Test si le nombre est pair ou impair
if nombre % 2 == 0:
    print(f"Le nombre {nombre} est pair.")
else:
    print(f"Le nombre {nombre} est impair.")
