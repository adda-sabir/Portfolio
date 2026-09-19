"""
seed_data.py
Pre-remplissage de la base de donnees Voodoo(r) avec des donnees
d'une usine de pieces automobiles.
Lancez ce script UNE SEULE FOIS apres avoir supprime l'ancien voodoo.db.
"""

from database import init_db, ajouter_machine, ajouter_produit, ajouter_tache, get_machines, get_produits

def seed():
    init_db()

    # ── 1. Machines ───────────────────────────────────────────────
    machines = [
        ("Presse a emboutir",   "Marc Dubois",   "ibraibth@gmail.com"),
        ("Tour CNC",            "Sophie Renard", "ibraibth@gmail.com"),
        ("Robot de soudure",    "Ahmed Karimi",  "ibraibth@gmail.com"),
        ("Convoyeur principal", "Julie Petit",   "ibraibth@gmail.com"),
        ("Fraiseuse CNC",       "Marc Dubois",   "ibraibth@gmail.com"),
        ("Cabine de peinture",  "Sophie Renard", "ibraibth@gmail.com"),
    ]

    print("Ajout des machines...")
    for nom, operateur, email in machines:
        ajouter_machine(nom, operateur, email)
        print(f"  OK {nom}")

    df_machines = get_machines()
    ids = {row["nom"]: int(row["id"]) for _, row in df_machines.iterrows()}


    # ── 2. Produits + Taches (puissance par tache) ────────────────
    produits = [
        {
            "nom": "Pare-chocs avant",
            "description": "Moulage, decoupe et finition pare-chocs ABS",
            "taches": [
                # (machine_id, puissance_W, duree_min, ordre)
                (ids["Presse a emboutir"],   50000, 45, 1),
                (ids["Tour CNC"],            10000, 20, 2),
                (ids["Cabine de peinture"],  12000, 60, 3),
                (ids["Convoyeur principal"],  3000, 10, 4),
            ]
        },
        {
            "nom": "Jante aluminium",
            "description": "Usinage et finition jante 17 pouces",
            "taches": [
                (ids["Tour CNC"],            10000, 60, 1),
                (ids["Fraiseuse CNC"],        8000, 45, 2),
                (ids["Tour CNC"],            10000, 20, 3),
                (ids["Convoyeur principal"],  3000, 10, 4),
            ]
        },
        {
            "nom": "Bras de suspension",
            "description": "Decoupe, soudure et traitement bras de suspension acier",
            "taches": [
                (ids["Presse a emboutir"],   50000, 30, 1),
                (ids["Robot de soudure"],    15000, 40, 2),
                (ids["Fraiseuse CNC"],        8000, 25, 3),
                (ids["Convoyeur principal"],  3000, 10, 4),
            ]
        },
        {
            "nom": "Boitier filtre a air",
            "description": "Emboutissage et assemblage boitier filtre moteur",
            "taches": [
                (ids["Presse a emboutir"],   50000, 20, 1),
                (ids["Robot de soudure"],    15000, 15, 2),
                (ids["Cabine de peinture"],  12000, 30, 3),
                (ids["Convoyeur principal"],  3000, 10, 4),
            ]
        },
    ]

    print("\nAjout des produits et taches...")
    for p in produits:
        produit_id = ajouter_produit(p["nom"], p["description"])#inserer le produit en base 
        print(f"  OK Produit : {p['nom']}")
        for machine_id, puissance, duree, ordre in p["taches"]:#inserer la tache en base liée au produit qu'on vient de creer 
            ajouter_tache(produit_id, machine_id, puissance, duree, ordre)
            machine_nom = df_machines.loc[df_machines["id"] == machine_id, "nom"].values[0]#filtre les lignes dont l'id correspond, "nom" sélectionne la colonne nom, .values[0] prend la première valeur trouvée.
            print(f"      -> Tache {ordre} : {machine_nom} ({puissance}W, {duree} min)")

    print("\nBase de donnees remplie avec succes !")
    print(f"   {len(machines)} machines | {len(produits)} produits | {sum(len(p['taches']) for p in produits)} taches")
    print("\nVous pouvez maintenant lancer main.py")


if __name__ == "__main__":
    seed()
