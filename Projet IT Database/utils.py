import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime, timedelta


def afficher_graphique(data):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data.index, data.values, color="royalblue", linewidth=1.5, label="Prix (EUR/MWh)")
    ax.fill_between(data.index, data.values, alpha=0.1, color="royalblue")

    negatifs = data[data < 0]
    if not negatifs.empty:
        ax.fill_between(data.index, data.values, 0,
                        where=(data.values < 0), color="red", alpha=0.3, label="Prix negatif")

    ax.set_title("Prix de l'electricite - zone BE (day-ahead)")
    ax.set_xlabel("Heure")
    ax.set_ylabel("EUR/MWh")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    plt.tight_layout()
    plt.show()


def verifier_prix_negatifs(data):
    negatifs = data[data < 0]
    if not negatifs.empty:
        heures = "\n".join(
            [f"{i.strftime('%H:%M')} -> {v:.2f} EUR/MWh" for i, v in zip(negatifs.index, negatifs.values)]
        )
        QMessageBox.information(
            None,
            "Prix negatifs detectes !",
            f"Les heures suivantes ont des prix negatifs :\n\n{heures}"
        )
    else:
        QMessageBox.information(None, "Dommage", "Aucun prix negatif detecte aujourd'hui.")


def calculer_cout_process(taches, heure_depart_str, prix_data):
    """
    Calcule le cout energetique total d'un process.
    Retourne (cout_total, detail).
    """
    today = datetime.now().date()
    curseur = datetime.strptime(heure_depart_str, "%H:%M").replace(
        year=today.year, month=today.month, day=today.day
    )#

    cout_total = 0.0
    detail = []

    for _, tache in taches.iterrows():
        puissance_w = float(tache["puissance"])
        duree_min = float(tache["duree"])
        machine_nom = tache["machine"]

        if puissance_w == 0:
            curseur += timedelta(minutes=duree_min)
            detail.append({
                "machine": machine_nom,
                "debut": curseur.strftime("%H:%M"),
                "duree_min": duree_min,
                "cout_eur": 0.0,
                "note": "forfait / hors-marche",
            })
            continue

        fin_tache = curseur + timedelta(minutes=duree_min)
        cout_tache = 0.0
        t = curseur

        while t < fin_tache:#on découpe chaque tâche en tranches de 15 minutes et on calcule le coût de chaque tranche séparément
            t_fin_tranche = min(t + timedelta(minutes=15), fin_tache) #min car on veut s'arreter a la fin si on a pas un multiple de 15
            duree_tranche_h = (t_fin_tranche - t).total_seconds() / 3600
            prix_eur_mwh = _prix_au_moment(prix_data, t)
            energie_kwh = (puissance_w / 1000) * duree_tranche_h
            cout_tache += energie_kwh * prix_eur_mwh / 1000
            t = t_fin_tranche

        cout_total += cout_tache
        detail.append({
            "machine": machine_nom,
            "debut": curseur.strftime("%H:%M"),
            "fin": fin_tache.strftime("%H:%M"),
            "duree_min": duree_min,
            "cout_eur": cout_tache,
        })
        curseur = fin_tache

    return cout_total, detail


def optimiser_heure_depart(taches, prix_data):
    """
    Teste toutes les heures de depart possibles (par tranche de 15 min)
    et retourne celle qui minimise le cout energetique.
    Retourne (meilleure_heure_str, cout_minimal).
    """
    duree_totale_min = taches["duree"].sum()
    meilleur_cout = float("inf") # impossible d'etre au dessus 
    meilleure_heure = "00:00"

    heure_max = 24 * 60 - int(duree_totale_min)
    for minutes in range(0, heure_max, 15):
        h = minutes // 60
        m = minutes % 60
        heure_str = f"{h:02d}:{m:02d}"
        try:
            cout, _ = calculer_cout_process(taches, heure_str, prix_data)
            if cout < meilleur_cout:
                meilleur_cout = cout
                meilleure_heure = heure_str
        except Exception:
            continue

    return meilleure_heure, meilleur_cout


def _construire_planning(taches_df, heure_depart_str):

    today = datetime.now().date()
    # On transforme "08:30" en un vrai datetime avec la date du jour
    curseur = datetime.strptime(heure_depart_str, "%H:%M").replace(
        year=today.year, month=today.month, day=today.day
    )

    planning = []
    for _, tache in taches_df.iterrows():
        duree_min = float(tache["duree"])
        fin = curseur + timedelta(minutes=duree_min)
        planning.append({
            "machine":   tache["machine"],
            "operateur": tache["operateur"],
            "debut":     curseur,
            "fin":       fin,
        })
        curseur = fin  # la tache suivante commence quand celle-ci se termine

    return planning


def verifier_disponibilite(commandes_existantes, nouvelles_taches, nouvelle_heure_depart):
    """
    
    conflits 
               Liste vide = aucun conflit, on peut enregistrer.
    """

    #  Etape 1 : construire le planning de la nouvelle commande 
    # On calcule les plages debut/fin de chaque tache du nouveau produit
    nouveau_planning = _construire_planning(nouvelles_taches, nouvelle_heure_depart)

    #  Etape 2 : construire le planning de toutes les commandes deja en place ─
    # Pour chaque commande deja enregistree dans la journee, on fait pareil
    planning_existant = []
    for commande in commandes_existantes:
        slots = _construire_planning(commande["taches"], commande["heure_depart"])
        # On ajoute le nom du produit pour pouvoir l'afficher dans le message
        for slot in slots:
            slot["produit"] = commande["produit_nom"]
        planning_existant.extend(slots)  # on ajoute tous ces slots a la liste globale

 
    conflits = []

    for nouveau_slot in nouveau_planning:
        for ancien_slot in planning_existant:

            # Verifier si les plages se chevauchent
            chevauchement = (
                nouveau_slot["debut"] < ancien_slot["fin"] and
                ancien_slot["debut"] < nouveau_slot["fin"]
            )

            if not chevauchement:
                continue  # pas de superposition temporelle, on passe au suivant

            # Les plages se chevauchent  est-ce la meme machine ?
            if nouveau_slot["machine"] == ancien_slot["machine"]:
                conflits.append(
                    f"Machine '{nouveau_slot['machine']}' deja occupee de "
                    f"{ancien_slot['debut'].strftime('%H:%M')} a "
                    f"{ancien_slot['fin'].strftime('%H:%M')} "
                    f"(produit : {ancien_slot['produit']})"
                )

            # Est-ce le meme operateur ? (on verifie separement pour avoir
            # un message precis meme si machine differente)
            elif nouveau_slot["operateur"] == ancien_slot["operateur"]:
                conflits.append(
                    f"Operateur '{nouveau_slot['operateur']}' deja assigne de "
                    f"{ancien_slot['debut'].strftime('%H:%M')} a "
                    f"{ancien_slot['fin'].strftime('%H:%M')} "
                    f"(produit : {ancien_slot['produit']}, "
                    f"machine : {ancien_slot['machine']})"
                )

    return conflits


def _prix_au_moment(prix_data, moment):
    """Retourne le prix EUR/MWh pour un instant donne (tranche quart-horaire)."""
    import pandas as pd

    if prix_data.index.tz is not None:
        import pytz
        tz = prix_data.index.tz
        moment_tz = pd.Timestamp(moment).tz_localize(tz) if moment.tzinfo is None else pd.Timestamp(moment).tz_convert(tz)
    else:
        moment_tz = pd.Timestamp(moment)

    try:
        idx = prix_data.index.asof(moment_tz) # 14h37 = 14H30
        if pd.isna(idx):
            return float(prix_data.iloc[0])
        return float(prix_data[idx])
    except Exception:
        return float(prix_data.iloc[0])
