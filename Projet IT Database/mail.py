import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os


def _get_smtp_config():
    load_dotenv()
    return {
        "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "user": os.getenv("SMTP_USER", ""),
        "password": os.getenv("SMTP_PASSWORD", ""),
    }


def _envoyer(destinataire, sujet, corps):
    """Fonction interne d'envoi générique."""
    cfg = _get_smtp_config()
    if not cfg["user"] or not cfg["password"]:
        return False, "Identifiants SMTP non configurés dans .env"

    msg = MIMEMultipart()
    msg["From"] = cfg["user"]
    msg["To"] = destinataire
    msg["Subject"] = sujet
    msg.attach(MIMEText(corps, "plain", "utf-8"))

    try:
        with smtplib.SMTP(cfg["host"], cfg["port"]) as serveur:
            serveur.ehlo() #salam au serveur (identification)
            serveur.starttls() #chiffre de la connexion
            serveur.login(cfg["user"], cfg["password"])
            serveur.sendmail(cfg["user"], destinataire, msg.as_string())
        return True, "Mail envoyé avec succès"
    except Exception as e:
        return False, str(e)


def envoyer_mail_operateur(destinataire, nom_operateur, taches_planifiees):
    """Envoie le planning à un opérateur."""
    if not destinataire:
        return False, "Adresse email vide"

    lignes = [
        f"Bonjour {nom_operateur},",
        "",
        "Voici votre emploi du temps pour la journée :",
        "",
    ]
    for t in taches_planifiees:
        lignes.append(
            f"  • {t['heure_debut']} – {t['heure_fin']}  |  "
            f"Machine : {t['machine']}  |  Produit : {t['produit']}  "
            f"({t['duree_min']} min)"
        )
    lignes += [
        "",
        "Merci de respecter ces horaires afin d'optimiser les coûts énergétiques.",
        "",
        "Cordialement,",
        "Voodoo® – Système de gestion énergétique",
    ]

    return _envoyer(destinataire, "Voodoo® – Votre planning du jour", "\n".join(lignes))


def envoyer_alerte_prix_negatifs(negatifs):
    """
    Dépassement ★ : envoie un mail d'alerte si des prix négatifs sont détectés.
    negatifs : pd.Series filtré (index=timestamps, values=prix)
    """
    load_dotenv()
    destinataire = os.getenv("SMTP_USER", "")
    if not destinataire:
        return False, "Email non configuré"

    lignes = [
        "⚠️ ALERTE – Prix négatifs détectés sur le marché belge !",
        "",
        "Les créneaux suivants ont des prix négatifs (vous êtes payé pour consommer) :",
        "",
    ]
    for ts, val in zip(negatifs.index, negatifs.values):
        lignes.append(f"  • {ts.strftime('%H:%M')}  →  {val:.2f} €/MWh")

    lignes += [
        "",
        "💡 Conseil : planifiez vos process les plus énergivores sur ces créneaux !",
        "",
        "Voodoo® – Système de gestion énergétique",
    ]

    return _envoyer(destinataire, "⚠️ Voodoo® – Alerte prix négatifs", "\n".join(lignes))


def envoyer_planning_complet(commandes_du_jour, prix_data):
    """Envoie le planning à tous les opérateurs impliqués."""
    from datetime import datetime, timedelta

    planning_operateurs = {}

    for commande in commandes_du_jour:
        heure_depart = datetime.strptime(commande["heure_depart"], "%H:%M")
        curseur = heure_depart

        for _, tache in commande["taches"].iterrows():
            duree_min = int(tache["duree"])
            heure_debut_str = curseur.strftime("%H:%M")
            heure_fin = curseur + timedelta(minutes=duree_min)
            heure_fin_str = heure_fin.strftime("%H:%M")

            email = tache["email"]
            if email and email not in planning_operateurs:
                planning_operateurs[email] = {"nom": tache["operateur"], "taches": []}

            if email:
                planning_operateurs[email]["taches"].append({
                    "produit": commande["produit_nom"],
                    "machine": tache["machine"],
                    "heure_debut": heure_debut_str,
                    "heure_fin": heure_fin_str,
                    "duree_min": duree_min,
                })

            curseur = heure_fin

    resultats = []
    for email, info in planning_operateurs.items():
        ok, msg = envoyer_mail_operateur(email, info["nom"], info["taches"])
        resultats.append({"email": email, "succes": ok, "message": msg})

    return resultats