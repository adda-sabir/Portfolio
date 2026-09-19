# Module généré par GenDB.py
#===========================
import sqlite3
import pandas as pd

def createAllTables():
	conn = sqlite3.connect("voodoo.db") #on ouvre la connexion à la base de donné  
	cur = conn.cursor() # curseur qui permet d'envoyer des commande sqlt 
	# produits #if si jms on relance eviter les soupes 
	cur.execute('''
			CREATE TABLE IF NOT EXISTS produits
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT,
				description TEXT
			)
			''')

	# machines
	cur.execute('''
			CREATE TABLE IF NOT EXISTS machines
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT NOT NULL,
				operateur TEXT,
				email TEXT
			)
			''')

	# taches
	cur.execute('''
			CREATE TABLE IF NOT EXISTS taches
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				produit_id INTEGER,
				machine_id INTEGER,
				puissance REAL,
				duree REAL,
				ordre INTEGER,
				FOREIGN KEY (produit_id) REFERENCES produits(id),
				FOREIGN KEY (machine_id) REFERENCES machines(id)
			)
			''')

	# commandes
	cur.execute('''
			CREATE TABLE IF NOT EXISTS commandes
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				produit_id INTEGER,
				heure_depart TEXT,
				cout_total REAL,
				date TEXT,
				FOREIGN KEY (produit_id) REFERENCES produits(id)
			)
			''')

	# prix_electricite
	cur.execute('''
			CREATE TABLE IF NOT EXISTS prix_electricite
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				date TEXT,
				heure TEXT,
				prix REAL
			)
			''')

	conn.commit() #sauvgarde confirmé 
	conn.close() 

def createTables_produits():
	conn = sqlite3.connect("voodoo.db") 
	cur = conn.cursor()
	# produits
	cur.execute('''
			CREATE TABLE IF NOT EXISTS produits
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT,
				description TEXT
			)
			''')
	conn.commit()
	conn.close()

def createTables_machines():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# machines
	cur.execute('''
			CREATE TABLE IF NOT EXISTS machines
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				nom TEXT NOT NULL,
				operateur TEXT,
				email TEXT
			)
			''')
	conn.commit()
	conn.close()

def createTables_taches():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# taches
	cur.execute('''
			CREATE TABLE IF NOT EXISTS taches
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				produit_id INTEGER,
				machine_id INTEGER,
				puissance REAL,
				duree REAL,
				ordre INTEGER,
				FOREIGN KEY (produit_id) REFERENCES produits(id),
				FOREIGN KEY (machine_id) REFERENCES machines(id)
			)
			''')
	conn.commit()
	conn.close()

def createTables_commandes():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# commandes
	cur.execute('''
			CREATE TABLE IF NOT EXISTS commandes
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				produit_id INTEGER,
				heure_depart TEXT,
				cout_total REAL,
				date TEXT,
				FOREIGN KEY (produit_id) REFERENCES produits(id)
			)
			''')
	conn.commit()
	conn.close()

def createTables_prix_electricite():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# prix_electricite
	cur.execute('''
			CREATE TABLE IF NOT EXISTS prix_electricite
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				date TEXT,
				heure TEXT,
				prix REAL
			)
			''')
	conn.commit()
	conn.close()


def insert_produits(nom,description):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO produits (nom,description) " #Construit la requête SQL. OR IGNORE → ignore l'insertion si doublon.
	sqlQuery+=f"VALUES ('{nom}','{description}')"
	cur.execute(sqlQuery) #execute la requete 
	produit_id = cur.lastrowid #Récupère l'ID auto-généré du produit qu'on vient d'insérer 
	conn.commit()
	conn.close()
	return produit_id


def insert_machines(nom,operateur,email):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO machines (nom,operateur,email) "
	sqlQuery+=f"VALUES ('{nom}','{operateur}','{email}')"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()


def insert_taches(produit_id,machine_id,puissance,duree,ordre):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO taches (produit_id,machine_id,puissance,duree,ordre) "
	sqlQuery+=f"VALUES ({produit_id},{machine_id},{puissance},{duree},{ordre})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()


def insert_commandes(produit_id,heure_depart,cout_total,date):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO commandes (produit_id,heure_depart,cout_total,date) "
	sqlQuery+=f"VALUES ({produit_id},'{heure_depart}',{cout_total},'{date}')"
	cur.execute(sqlQuery)
	commande_id = cur.lastrowid
	conn.commit()
	conn.close()
	return commande_id


def insert_prix_electricite(date,heure,prix):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO prix_electricite (date,heure,prix) "
	sqlQuery+=f"VALUES ('{date}','{heure}',{prix})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

def select_produits(WHERE=""):
	conn = sqlite3.connect("voodoo.db")
	sqlQuery="SELECT id,nom,description FROM produits"
	if WHERE.strip()!="":  #est ce que where contient autres chose que des espace  et si il est vide il return toutes les produit  sinon jproduits uste le numero 
		sqlQuery+=f" WHERE {WHERE}"
	df = pd.read_sql_query(sqlQuery, conn) #on rends lisible la reponse de la requete et la renvoie une dataframe
	conn.close()
	return df # renvoie le tableau 

# SELECT fields FROM machines WHERE condition
def select_machines(WHERE=""):
	conn = sqlite3.connect("voodoo.db")
	sqlQuery="SELECT id,nom,operateur,email FROM machines"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	df = pd.read_sql_query(sqlQuery, conn)
	conn.close()
	return df


# Le JOIN sert à fusionner ces deux tables en une seule au moment de la requête, en faisant correspondre les lignes qui partagent le même identifiant :
def select_taches(WHERE=""):
	conn = sqlite3.connect("voodoo.db") #Quand deux tables sont jointes, certains noms de colonnes peuvent exister dans les deux. Les préfixes permettent de lever l'ambiguïté :
	sqlQuery="""SELECT t.id,t.ordre,t.puissance,t.duree,m.nom AS machine,m.operateur,m.email
        FROM taches t
        JOIN machines m ON t.machine_id = m.id"""
	if WHERE.strip()!="": 
		sqlQuery += f" WHERE {WHERE} ORDER BY t.ordre" #retire les espaces en début et fin de chaîne, pour éviter qu'un appel comme select_taches("   ") soit traité comme un vrai filtre. Si après nettoyage la chaîne n'est pas vide, le filtre est collé à la fin de la requête SQL.
#Le f"..." est un f-string : il permet d'insérer la valeur de WHERE directement dans la chaîne de texte.
	df = pd.read_sql_query(sqlQuery, conn)
	conn.close()
	return df


def select_commandes(WHERE=""):
	conn = sqlite3.connect("voodoo.db")
	sqlQuery="""SELECT c.id,p.nom AS produit,c.heure_depart,c.cout_total,c.date
        FROM commandes c
        JOIN produits p ON c.produit_id = p.id"""
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	sqlQuery+=" ORDER BY c.heure_depart"
	df = pd.read_sql_query(sqlQuery, conn)
	conn.close()
	return df


def select_prix_electricite(WHERE=""):
	conn = sqlite3.connect("voodoo.db")
	sqlQuery="SELECT id,date,heure,prix FROM prix_electricite"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	df = pd.read_sql_query(sqlQuery, conn)
	conn.close()
	return df


def update_produits(id,nom,description,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	cur.execute(
		"UPDATE produits SET nom=?, description=? WHERE id=?",
		(nom, description, id)
	) #Envoie la requête SQL de mise à jour. Explication détaillée juste en dessous
	conn.commit()
	conn.close()


def update_machines(id,nom,operateur,email,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	cur.execute(
		"UPDATE machines SET nom=?, operateur=?, email=? WHERE id=?",
		(nom, operateur, email, id)
	)
	conn.commit()
	conn.close()


def update_taches(id,produit_id,machine_id,puissance,duree,ordre,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	cur.execute(
		"UPDATE taches SET produit_id=?, machine_id=?, puissance=?, duree=?, ordre=? WHERE id=?",
		(produit_id, machine_id, puissance, duree, ordre, id)
	)
	conn.commit()
	conn.close()

def update_commandes(id,produit_id,heure_depart,cout_total,date,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	cur.execute(
		"UPDATE commandes SET produit_id=?, heure_depart=?, cout_total=?, date=? WHERE id=?",
		(produit_id, heure_depart, cout_total, date, id)
	)
	conn.commit()
	conn.close()


def update_prix_electricite(id,date,heure,prix,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE prix_electricite SET date='{date}',heure='{heure}',prix={prix}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()


def delete_produits(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM produits" #on va delet tout ici 
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}" # et là si on supprime en focntion de l id 
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()


def delete_machines(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM machines"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()


def delete_taches(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM taches"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

def delete_commandes(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM commandes"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

def delete_prix_electricite(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM prix_electricite"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()


def drop_produits():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE produits"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

def drop_machines():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE machines"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()


#  detruit la table elle doit  etre recreee
def drop_taches():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE taches"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

def drop_commandes():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE commandes"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()


def drop_prix_electricite():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE prix_electricite"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()




def init_db():
	createAllTables()

def sauvegarder_prix(prix_series, date_str): #Reçoit deux paramètres : une Series pandas contenant les prix heure par heure, et une date sous forme de texte comme "2024-01-15".
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	cur.execute("DELETE FROM prix_electricite WHERE date = ?", (date_str,)) #Avant d'insérer quoi que ce soit, on supprime les données déjà existantes pour cette date. Ça évite les doublons si on appelle la fonction deux fois pour la même journée.
	for timestamp, prix in zip(prix_series.index, prix_series.values): #Convertit le timestamp complet en simple texte d'heure. strftime est une fonction de formatage de date — %H = heure, %M = minutes. Donc 2024-01-15 08:00:00 devient "08:00"
		heure_str = timestamp.strftime("%H:%M")
		cur.execute(
			"INSERT INTO prix_electricite (date, heure, prix) VALUES (?, ?, ?)",
			(date_str, heure_str, float(prix))
		)
	conn.commit()
	conn.close()

def charger_prix_db(date_str):
	conn = sqlite3.connect("voodoo.db")
	df = pd.read_sql_query(
		"SELECT heure, prix FROM prix_electricite WHERE date = ? ORDER BY heure",
		conn, params=(date_str,)
	)
	conn.close()
	if df.empty:
		return None
	return pd.Series(df["prix"].values, index=df["heure"].values) ##Récupère toutes les lignes de la date demandée, triées par heure. Le résultat est un DataFrame avec deux colonnes : heure et prix. Le params=(date_str,) est l'équivalent des ? — même principe de sécurité qu'on a vu dans delete_produits.

def ajouter_machine(nom, operateur, email):
	insert_machines(nom, operateur, email)

def ajouter_produit(nom, description):
	return insert_produits(nom, description)

def ajouter_tache(produit_id, machine_id, puissance, duree, ordre):
	insert_taches(produit_id, machine_id, puissance, duree, ordre)

def ajouter_commande(produit_id, heure_depart, cout_total, date):
	return insert_commandes(produit_id, heure_depart, cout_total, date)

def get_machines():
	return select_machines()

def get_produits():
	return select_produits()

def get_taches_produit(produit_id):
	return select_taches(f"t.produit_id = {produit_id}")

def get_commandes():
	return select_commandes()

def get_produit_by_id(produit_id):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	cur.execute("SELECT * FROM produits WHERE id = ?", (produit_id,))
	row = cur.fetchone() #chope une ligne dans dataframe
	conn.close()
	return row

def supprimer_commandes_jour(date):
	delete_commandes(f"date = '{date}'")

def get_all_taches():
	conn = sqlite3.connect("voodoo.db")
	df = pd.read_sql_query("""
		SELECT t.id, t.ordre, t.puissance, t.duree,
		       m.nom AS machine, m.operateur,
		       p.nom AS produit
		FROM taches t
		JOIN machines m ON t.machine_id = m.id
		JOIN produits p ON t.produit_id = p.id
		ORDER BY p.nom, t.ordre
	""", conn)
	conn.close()
	return df
