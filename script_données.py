import pandas as pd
import numpy as np

# Fonction pour lire différents formats de fichiers
def read_file(filepath):
    print(f"Chemin du fichier source : {filepath}")
    if filepath.endswith('.csv'):
        fichier = pd.read_csv(filepath)
    elif filepath.endswith('.json'):
        fichier = pd.read_json(filepath)
    elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
        fichier = pd.read_excel(filepath)
    elif filepath.endswith('.parquet'):
        fichier = pd.read_parquet(filepath)
    else:
        raise ValueError(f"Format de fichier non pris en charge : {filepath}")
    return fichier

# Fonction pour nettoyer le DataFrame
def clean_file(fichier, list_strategy):
    print("Nettoyage des données en cours...")

    if len(list_strategy) != len(fichier.columns):
        raise ValueError("La longueur de list_strategy doit correspondre au nombre de colonnes dans le DataFrame.")

    for i, column in enumerate(fichier.columns):
        strategy = list_strategy[i]

        if strategy == 'mean':
            fichier[column] = pd.to_numeric(fichier[column], errors='coerce')
            value = fichier[column].mean()
            fichier[column] = fichier[column].fillna(value)

        elif strategy == 'median':
            fichier[column] = pd.to_numeric(fichier[column], errors='coerce')
            value = fichier[column].median()
            fichier[column] = fichier[column].fillna(value)

        elif strategy == 'no_change':
            pass

        else:
            fichier[column] = fichier[column].fillna(strategy)

    fichier = fichier.dropna()
    fichier = fichier.drop_duplicates()
    fichier = fichier.reset_index(drop=True)

    print("Nettoyage terminé.")
    return fichier


# Inputs interactifs pour les chemins
filepath = input("Entrez le chemin du fichier source : ").strip()
output_path = input("Entrez le chemin pour sauvegarder le fichier nettoyé : ").strip()

# Lire le fichier
fichier = read_file(filepath)


print("=== Configuration des stratégies pour chaque colonne ===")
print("========================================================")
list_strategy = []
for column in fichier.columns:
    strategy = input(f"Colonne : {column} - Remplissage (mean, median, no_change, ou une string spécifique) : ").strip()
    list_strategy.append(strategy)

# Appliquer la stratégie de nettoyage
fichier = clean_file(fichier=fichier, list_strategy=list_strategy)

# Sauvegarder le fichier nettoyé
fichier.to_csv(output_path)
print(f"Fichier nettoyé sauvegardé avec succès à : {output_path}")
