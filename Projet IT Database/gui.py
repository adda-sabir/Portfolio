import os
from PyQt6.QtWidgets import (
    QWidget, QTabWidget, QApplication, QMessageBox,
    QTableWidgetItem, QDialog, QDialogButtonBox,
    QFormLayout, QLineEdit, QComboBox, QSpinBox, QInputDialog
)
from PyQt6 import uic
from PyQt6.QtCore import Qt, QTime
from datetime import datetime, timedelta
from PyQt6.QtGui import QMovie
from database import (
    ajouter_machine, ajouter_produit, ajouter_tache, ajouter_commande,
    get_machines, get_produits, get_taches_produit, get_commandes,
    get_all_taches, delete_machines, delete_produits, delete_taches,
    update_machines, update_produits, update_taches
)
from entsoe_api import charger_prix_entsoe
from utils import afficher_graphique, verifier_prix_negatifs, calculer_cout_process, optimiser_heure_depart, verifier_disponibilite
from mail import envoyer_planning_complet, envoyer_alerte_prix_negatifs

# Chemin vers le fichier .ui (même dossier que gui.py)
UI_FILE = os.path.join(os.path.dirname(__file__), "voodoo.ui")


# ── Dialogues de modification ──────────────────────────────────────────────────

class DialogModifierMachine(QDialog):
    def __init__(self, id_, nom, operateur, email, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Modifier machine id={id_}")
        self.id_ = id_
        layout = QFormLayout()
        self.nomM  = QLineEdit(nom)
        self.operM = QLineEdit(operateur)
        self.mailM = QLineEdit(email)
        layout.addRow("Nom machine :", self.nomM)
        layout.addRow("Opérateur :",   self.operM)
        layout.addRow("Email :",        self.mailM)
        boutons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                   QDialogButtonBox.StandardButton.Cancel)
        boutons.accepted.connect(self.accept)
        boutons.rejected.connect(self.reject)
        layout.addRow(boutons)
        self.setLayout(layout)

    def valeurs(self):
        return self.nomM.text(), self.operM.text(), self.mailM.text()


class DialogModifierProduit(QDialog):
    def __init__(self, id_, nom, description, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Modifier produit id={id_}")
        self.id_ = id_
        layout = QFormLayout() #organise les champs en deux collones label à gauche et champ à droite 
        self.nomP  = QLineEdit(nom)#champ de text libre 
        self.descP = QLineEdit(description)#champ de text libre 
        layout.addRow("Nom produit :", self.nomP)
        layout.addRow("Description :", self.descP)
        boutons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                   QDialogButtonBox.StandardButton.Cancel)
        boutons.accepted.connect(self.accept)
        boutons.rejected.connect(self.reject)
        layout.addRow(boutons)
        self.setLayout(layout)#affiche tous ces éléments dans cette fenêtre, dans cet ordre sans ca la fenetre s'ouvre mais elle est vide

    def valeurs(self):
        return self.nomP.text(), self.descP.text()


class DialogModifierTache(QDialog):# fenetre pop up 
    def __init__(self, id_, ordre, puissance, duree, machine_nom, produit_nom,
                 machines_df, produits_df, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Modifier tâche id={id_}")
        self.id_ = id_
        layout = QFormLayout()

        self.comboProduit = QComboBox() #menu déroulant
        for _, row in produits_df.iterrows(): #parcours la df ligne par ligne 
            self.comboProduit.addItem(row["nom"], userData=int(row["id"])) #row nom est pour l'utilisateur masi le row id est pour retrouver l'id quand il a fait son choix 
            if row["nom"] == produit_nom:#Sans ces deux lignes, le menu s'ouvrirait toujours sur "Engrenage" peu importe quelle tâche tu modifies.
                self.comboProduit.setCurrentIndex(self.comboProduit.count() - 1)

        self.comboMachine = QComboBox() 
        for _, row in machines_df.iterrows():
            self.comboMachine.addItem(row["nom"], userData=int(row["id"]))
            if row["nom"] == machine_nom:
                self.comboMachine.setCurrentIndex(self.comboMachine.count() - 1)

        self.puissT = QSpinBox() #champ numérique avec flèches haut/bas
        self.puissT.setRange(0, 500000)
        self.puissT.setSuffix(" W")
        self.puissT.setValue(int(float(puissance)))

        self.dureeT = QSpinBox()
        self.dureeT.setRange(1, 1440)
        self.dureeT.setSuffix(" min")
        self.dureeT.setValue(int(float(duree)))

        self.ordreT = QSpinBox()
        self.ordreT.setRange(1, 99)
        self.ordreT.setValue(int(ordre))

        layout.addRow("Produit :",               self.comboProduit)
        layout.addRow("Machine :",               self.comboMachine)
        layout.addRow("Puissance (W) :",         self.puissT)
        layout.addRow("Durée :",                 self.dureeT)
        layout.addRow("Ordre dans le process :", self.ordreT)

        boutons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                   QDialogButtonBox.StandardButton.Cancel)
        boutons.accepted.connect(self.accept)
        boutons.rejected.connect(self.reject)
        layout.addRow(boutons)
        self.setLayout(layout)

    def valeurs(self):
        return (self.comboProduit.currentData(),
                self.comboMachine.currentData(),
                self.puissT.value(),
                self.dureeT.value(),
                self.ordreT.value())


# ── Fenêtre principale ─────────────────────────────────────────────────────────

class FenetrePrincipale(QTabWidget): # donne les postion qu'on a choisis dans qdesigner de chaque bouton 
    def __init__(self):
        super().__init__()

        # Charge la structure visuelle depuis le fichier .ui
        uic.loadUi(UI_FILE, self)

        self.prix_data = None

        # Affichage de la date en coin
        date_du_jour = datetime.now().strftime("%d/%m/%Y")
        self.label_date.setText(f"📅 {date_du_jour}")

        # Connexions onglet Configuration 
        self.btnAjouterMachine.clicked.connect(self.ajouter_machine)
        self.btnAjouterProduit.clicked.connect(self.ajouter_produit)
        self.btnAjouterTache.clicked.connect(self.ajouter_tache)
        self.btnActualiser.clicked.connect(self.refresh_all)

        self.btnModifierMachine.clicked.connect(self.modifier_machine)
        self.btnSupprimerMachine.clicked.connect(self.supprimer_machine)
        self.btnModifierProduit.clicked.connect(self.modifier_produit)
        self.btnSupprimerProduit.clicked.connect(self.supprimer_produit)
        self.btnModifierTache.clicked.connect(self.modifier_tache)
        self.btnSupprimerTache.clicked.connect(self.supprimer_tache)
        
        # Connexions onglet Commandes
        self.btnChargerPrix.clicked.connect(self.charger_prix)
        self.btnVerifierAlertes.clicked.connect(self.check_alertes)
        self.btnCalculer.clicked.connect(self.calculer_et_enregistrer)
        self.btnEnvoyerMails.clicked.connect(self.envoyer_mails)
        self.btnActualiserCommandes.clicked.connect(self.refresh_commandes)
        self.checkOptimiser.stateChanged.connect(self._toggle_heure)
        self.btnnoter.clicked.connect(self.ouvrir_notation)
        self.currentChanged.connect(self._on_tab_changed)
        self.btnVerifierSeuil.clicked.connect(self.verifier_seuil)

        self.refresh_all()
        self.refresh_produits()
        self.refresh_commandes()
        


    #  Helpers 
    
    def _remplir(self, tab, df):
        tab.setRowCount(len(df)) #taille tablleau 
        tab.setColumnCount(len(df.columns))
        tab.setHorizontalHeaderLabels(list(df.columns))
        for i in range(len(df)): #parcours celulle ligne collone 
            for j, c in enumerate(df.columns):
                item = QTableWidgetItem(str(df.iloc[i][c])) #objet PyQt qui représnte une cellule dans un tableau visuel
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)#impossible à edit 
                tab.setItem(i, j, item)
        tab.resizeColumnsToContents()
        tab.horizontalHeader().setStretchLastSection(True) #ajuster la taille pour que le texte rentre bien 
        hauteur = 30 * tab.rowCount() + tab.horizontalHeader().height() + 10 #fixer une hauteur adapter au nombre de ligne 
        tab.setMinimumHeight(min(max(hauteur, 200), 400))
    
    def _id_ligne_selectionnee(self, table):
        rows = table.selectionModel().selectedRows()
        if not rows:
            return None, None
        row = rows[0].row()
        return int(table.item(row, 0).text()), row

    def _toggle_heure(self, state):
        self.heureDepart.setEnabled(state != Qt.CheckState.Checked)

    def _on_tab_changed(self, index):
        if index == 1:
            self.refresh_produits()

    # ── Refresh ───────────────────────────────────────────────────

    def refresh_all(self):
        machines = get_machines()
        produits = get_produits()
        taches   = get_all_taches()

        self._remplir(self.tableMachines, machines)
        self._remplir(self.tableProduits, produits)
        self._remplir(self.tableTaches,   taches)

        self.comboProduitT.clear()
        for _, row in produits.iterrows():
            self.comboProduitT.addItem(row["nom"], userData=int(row["id"]))

        self.comboMachineT.clear()
        for _, row in machines.iterrows():
            self.comboMachineT.addItem(row["nom"], userData=int(row["id"]))

    def refresh_produits(self):
        self.comboProduit.clear()
        for _, row in get_produits().iterrows():
            self.comboProduit.addItem(row["nom"], userData=int(row["id"]))

    def refresh_commandes(self):
        df = get_commandes()
        self.tableCommandes.setRowCount(len(df))
        self.tableCommandes.setColumnCount(len(df.columns))
        self.tableCommandes.setHorizontalHeaderLabels(list(df.columns))
        for i in range(len(df)):
            for j, c in enumerate(df.columns):
                val = df.iloc[i][c]
                if c == "cout_total":
                    val = f"{float(val):.4f} €"
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.tableCommandes.setItem(i, j, item)
        self.tableCommandes.resizeColumnsToContents()
        self.tableCommandes.horizontalHeader().setStretchLastSection(True)

    # ── Ajouts ────────────────────────────────────────────────────

    def ajouter_machine(self):
        if not self.nomM.text():
            QMessageBox.warning(self, "Erreur", "Nom de la machine obligatoire.")
            return
        ajouter_machine(self.nomM.text(), self.operM.text(), self.mailM.text())
        self.refresh_all()
        for champ in [self.nomM, self.operM, self.mailM]:
            champ.clear()

    def ajouter_produit(self):
        if not self.nomP.text():
            QMessageBox.warning(self, "Erreur", "Nom du produit obligatoire.")
            return
        ajouter_produit(self.nomP.text(), self.descP.text())
        self.refresh_all()
        for champ in [self.nomP, self.descP]:
            champ.clear()

    def ajouter_tache(self):
        if self.comboProduitT.count() == 0 or self.comboMachineT.count() == 0:
            QMessageBox.warning(self, "Erreur", "Ajoutez d'abord des produits et machines.")
            return
        ajouter_tache(self.comboProduitT.currentData(),
                      self.comboMachineT.currentData(),
                      self.puissT.value(),
                      self.dureeT.value(),
                      self.ordreT.value())
        self.refresh_all()
        QMessageBox.information(self, "OK", "Tâche ajoutée avec succès.")

    # ── Modifications ─────────────────────────────────────────────

    def modifier_machine(self):
        id_, row = self._id_ligne_selectionnee(self.tableMachines)
        if id_ is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une machine dans le tableau.")
            return
        nom  = self.tableMachines.item(row, 1).text()
        oper = self.tableMachines.item(row, 2).text()
        mail = self.tableMachines.item(row, 3).text()
        dlg = DialogModifierMachine(id_, nom, oper, mail, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            n, o, m = dlg.valeurs()
            if not n:
                QMessageBox.warning(self, "Erreur", "Nom obligatoire.")
                return
            update_machines(id_, n, o, m, "")
            self.refresh_all()

    def modifier_produit(self):
        id_, row = self._id_ligne_selectionnee(self.tableProduits)
        if id_ is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un produit dans le tableau.")
            return
        nom  = self.tableProduits.item(row, 1).text()
        desc = self.tableProduits.item(row, 2).text()
        dlg = DialogModifierProduit(id_, nom, desc, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            n, d = dlg.valeurs()
            if not n:
                QMessageBox.warning(self, "Erreur", "Nom obligatoire.")
                return
            update_produits(id_, n, d, "")
            self.refresh_all()

    def modifier_tache(self):
        id_, row = self._id_ligne_selectionnee(self.tableTaches)
        if id_ is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une tâche dans le tableau.")
            return
        ordre   = self.tableTaches.item(row, 1).text()
        puiss   = self.tableTaches.item(row, 2).text()
        duree   = self.tableTaches.item(row, 3).text()
        machine = self.tableTaches.item(row, 4).text()
        produit = self.tableTaches.item(row, 6).text()
        dlg = DialogModifierTache(id_, ordre, puiss, duree, machine, produit,
                                  get_machines(), get_produits(), self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            prod_id, mach_id, pui, dur, ord_ = dlg.valeurs()
            update_taches(id_, prod_id, mach_id, pui, dur, ord_, "")
            self.refresh_all()

    # ── Suppressions ──────────────────────────────────────────────

    def supprimer_machine(self):
        id_, _ = self._id_ligne_selectionnee(self.tableMachines)
        if id_ is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une machine dans le tableau.")
            return
        rep = QMessageBox.question(self, "Confirmer",
            f"Supprimer la machine id={id_} ?\nSes tâches associées seront aussi supprimées.")
        if rep == QMessageBox.StandardButton.Yes:
            delete_taches(f"machine_id = {id_}")
            delete_machines(f"id = {id_}")
            self.refresh_all()

    def supprimer_produit(self):
        id_, _ = self._id_ligne_selectionnee(self.tableProduits)
        if id_ is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un produit dans le tableau.")
            return
        rep = QMessageBox.question(self, "Confirmer",
            f"Supprimer le produit id={id_} ?\nSes tâches associées seront aussi supprimées.")
        if rep == QMessageBox.StandardButton.Yes:
            delete_taches(f"produit_id = {id_}")
            delete_produits(f"id = {id_}")
            self.refresh_all()

    def supprimer_tache(self):
        id_, _ = self._id_ligne_selectionnee(self.tableTaches)
        if id_ is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une tâche dans le tableau.")
            return
        rep = QMessageBox.question(self, "Confirmer", f"Supprimer la tâche id={id_} ?")
        if rep == QMessageBox.StandardButton.Yes:
            delete_taches(f"id = {id_}")
            self.refresh_all()

    #  Prix et Commandes 

    def charger_prix(self):
        try:
            self.prix_data = charger_prix_entsoe() #series pandas avec le prix de l'elec 
            afficher_graphique(self.prix_data) #affiche le graphique
        except Exception as e:
            QMessageBox.critical(self, "Erreur ENTSO-E", str(e))

    def check_alertes(self):
        try:
            if self.prix_data is None: #si le prix a pas été chargé 
                self.prix_data = charger_prix_entsoe()
            verifier_prix_negatifs(self.prix_data) 
            negatifs = self.prix_data[self.prix_data < 0] 
            if not negatifs.empty: 
                ok, msg = envoyer_alerte_prix_negatifs(negatifs)
                if ok:
                    QMessageBox.information(self, "📧 Mail envoyé",
                        "Une alerte a aussi été envoyée par mail !")
                else:
                    QMessageBox.warning(self, "Mail non envoyé",
                        f"Popup affichée mais mail échoué :\n{msg}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def calculer_et_enregistrer(self):
        if self.comboProduit.count() == 0: #si aucun produit n'existe ne base on arret tout 
            QMessageBox.warning(self, "Erreur", "Aucun produit disponible.")
            return
        if self.prix_data is None:
            try:
                self.prix_data = charger_prix_entsoe()
            except Exception as e:
                QMessageBox.critical(self, "Erreur ENTSO-E", str(e))
                return

        produit_id  = self.comboProduit.currentData()
        produit_nom = self.comboProduit.currentText()
        taches = get_taches_produit(produit_id)
        if taches.empty:
            QMessageBox.warning(self, "Erreur", "Ce produit n'a aucune tâche définie.")
            return

        if self.checkOptimiser.isChecked(): # depend de si onclique ou pas sur prix optimisé
            try:
                heure_str, cout_min = optimiser_heure_depart(taches, self.prix_data)
                self.heureDepart.setTime(QTime.fromString(heure_str, "HH:mm"))
                QMessageBox.information(self, "⚡ Heure optimisée",
                    f"Meilleure heure de départ : {heure_str}\n"
                    f"Coût minimal estimé : {cout_min:.4f} €")
            except Exception as e:
                QMessageBox.critical(self, "Erreur optimisation", str(e))
                return
        else:
            heure_str = self.heureDepart.time().toString("HH:mm")
#depasse pas minuit s verification
        duree_totale    = taches["duree"].sum()
        heure_depart_dt = datetime.strptime(heure_str, "%H:%M")
        heure_fin_dt    = heure_depart_dt + timedelta(minutes=duree_totale)
        if heure_fin_dt.date() > heure_depart_dt.date():
            QMessageBox.warning(self, "Hors journée",
                f"Ce process dure {int(duree_totale)} min et se terminerait à "
                f"{heure_fin_dt.strftime('%H:%M')}, après minuit !\n"
                "Choisissez une heure de départ plus tôt.")
            return

        try:
            cout, detail = calculer_cout_process(taches, heure_str, self.prix_data)
        except Exception as e:
            QMessageBox.critical(self, "Erreur calcul", str(e))
            return

        # Verification de disponibilite
        commandes_df = get_commandes()
        commandes_existantes = []
        for _, row in commandes_df.iterrows():
            produits_df = get_produits()
            match = produits_df.loc[produits_df["nom"] == row["produit"], "id"]
            if match.empty:
                continue
            pid = int(match.values[0])
            commandes_existantes.append({
                "produit_nom":  row["produit"],
                "heure_depart": row["heure_depart"],
                "taches":       get_taches_produit(pid),
            })

        conflits = verifier_disponibilite(commandes_existantes, taches, heure_str)
        if conflits:
            lignes_conflits = ["Impossible d enregistrer cette commande :", ""]
            for c in conflits:
                lignes_conflits.append("  - " + c)
            lignes_conflits.append("")
            lignes_conflits.append("Modifiez l heure de depart ou choisissez un autre produit.")
            QMessageBox.warning(self, "Conflit de disponibilite", "\n".join(lignes_conflits))
            return
        date_today = datetime.now().strftime("%Y-%m-%d")
        ajouter_commande(produit_id, heure_str, cout, date_today)
        self.labelCout.setText(f"OK {produit_nom} a {heure_str}  ->  Cout estime : {cout:.4f} EUR")
        self.refresh_commandes()

    def envoyer_mails(self):
        commandes_df = get_commandes()
        if commandes_df.empty:
            QMessageBox.information(self, "Info", "Aucune commande enregistrée aujourd'hui.")
            return
        if self.prix_data is None:
            try:
                self.prix_data = charger_prix_entsoe()
            except Exception as e:
                QMessageBox.critical(self, "Erreur ENTSO-E", str(e))
                return

        commandes_list = []
        for _, row in commandes_df.iterrows():
            produits_df = get_produits()
            match = produits_df.loc[produits_df["nom"] == row["produit"], "id"]
            if match.empty:
                continue
            produit_id = int(match.values[0])
            taches = get_taches_produit(produit_id)
            commandes_list.append({
                "produit_nom":  row["produit"],
                "heure_depart": row["heure_depart"],
                "taches":       taches,
            })

        resultats = envoyer_planning_complet(commandes_list, self.prix_data)
        resume = "\n".join(
            [f"{'✅' if r['succes'] else '❌'} {r['email']} : {r['message']}"
             for r in resultats])
        QMessageBox.information(self, "Résultat envoi mails",
            resume if resume else "Aucun opérateur à notifier.")
    def ouvrir_notation(self):
        note, ok = QInputDialog.getInt(self, "Notation",
            "Entrez la note sur 20 :",
            min=0, max=20)
        if ok:
            QMessageBox.information(self, "Note enregistrée",
                f"Note : {note}/20 ✅")
            self.movie = QMovie("merci.gif")
            self.labelGif.setMovie(self.movie)
            self.movie.start()
    def verifier_seuil(self):
        if self.prix_data is None:
            QMessageBox.warning(self, "Pas de prix",
                "Aucune donnee de prix disponible.\n"
                "Cliquez d'abord sur 'Charger les prix'.")
            return

        seuil = self.spinSeuilPrix.value()

        au_dessus = self.prix_data[self.prix_data > seuil]

        if au_dessus.empty:
            QMessageBox.information(
                self,
                "Seuil respecte",
                f"Aucune tranche horaire ne depasse {seuil} EUR/MWh aujourd'hui.\n"
                "Vous pouvez planifier librement."
            )
        else:
            lignes = [f"ATTENTION : {len(au_dessus)} creneau(x) depassent {seuil} EUR/MWh :\n"]
            for ts, val in zip(au_dessus.index, au_dessus.values):
                try:
                    heure_str = ts.strftime("%H:%M")
                except AttributeError:
                    heure_str = str(ts)
                lignes.append(f"  - {heure_str}  ->  {val:.2f} EUR/MWh")
            lignes.append(f"\nConseil : evitez de lancer vos machines sur ces creneaux.")
            QMessageBox.warning(
                self,
                f"Seuil {seuil} EUR/MWh depasse !",
                "\n".join(lignes)
            )