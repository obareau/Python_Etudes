"""
Programme qui permet de savoir si un nombre est premier ou non"""


# Fonction pour vérifier si un nombre est premier
def est_premier(nombre):
    """Indique si un nombre est premier.

    Un nombre est premier s'il n'a que deux diviseurs : 1 et lui-même.
    La fonction utilise un algorithme de trial division pour tester
    les diviseurs jusqu'à la racine carrée du nombre.

    Parameters
    ----------
    nombre : int
        Le nombre à tester.

    Returns
    -------
    bool
        True si le nombre est premier, False sinon.
    """
    if nombre <= 1:
        return False
    for i in range(2, int(nombre**0.5) + 1):
        if nombre % i == 0:
            return False
    return True


# Demande à l'utilisateur d'entrer un nombre
nombre = int(input("Entrez un nombre : "))

# Liste des diviseurs à tester
diviseurs = [
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    11,
    13,
    15,
    17,
    19,
    21,
    23,
    25,
    27,
    29,
    31,
    33,
    35,
    37,
    39,
    41,
    43,
    45,
    47,
    49,
    51,
    53,
    55,
    57,
    59,
    61,
    63,
    65,
    67,
    69,
    71,
    73,
    75,
    77,
    79,
    81,
    83,
    85,
    87,
    89,
    91,
    93,
    95,
    97,
    99,
]

# Test de divisibilité
print(f"\nRésultats pour le nombre {nombre} :")
for diviseur in diviseurs:
    if nombre % diviseur == 0:
        print(f"- Divisible par {diviseur}")
    else:
        print(f"- Non divisible par {diviseur}")

# Test si le nombre est premier
if est_premier(nombre):
    print(f"\nLe nombre {nombre} est un nombre premier.")
else:
    print(f"\nLe nombre {nombre} n'est pas un nombre premier.")
