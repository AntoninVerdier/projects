# Algorithme d’affectation des tuteurs par la méthode de Kuhn-Munkres

## Version 2.0 

/!\ Ce fichier est en cours d’écriture.

Ce programme fonctionne sur la base d’un dossier contenant les voeux des tuteurs, d’un fichier .py et d’un fichier de paramètre.

### Récupération des données

La récupération des voeux des tuteurs se fait via Plesk en entrant dans la base de donnée associée à tutoweb.org. Il est nécessaire de télécharger au format `.csv` la table "voeux".

Une fois téléchargée, ce fichier `.csv` doit être scindé en trois fichiers distincts de noms différents, par exemple : `voeux_R.csv`, `voeux_P.csv` et `voeux_M.csv`. Chaque fichier doit contenir les voeux correspondants à une seule faculté.

Déposer ces fichiers correctement renommés et au format `.csv` dans le dossier "Data".

### Paramètrage

Il s’effectue dans le fichier `settings_pref_params.py` dans le dossier "Code". Dans un premier temps, renseigner le nom du fichier à ligne `self.path2csv = 'Data/voeux_R.csv`en remplaçant "voeux_R" par le nom d’un de vos trois fichiers.

Renseignez la ligne  `self.nb_matiere_rangs = [19, 18, 19, 10, 12, 11, 20, 20]` en remplaçant chaque nombre par le nombre voulu d’étudiant dans la matière correspondante. La correspondance avec les matières est donnée par la ligne : `	self.liste_matiere_rangs = [101, 102, 103, 202, 204, 205, 301, 401]` de manière à ce que la première matière soit la 101, la seconde la 102 etc. Le code est disponible en commentaire en haut du fichier.

Enfin, renseigner `True` à la ligne `		self.rangs = True` et `False` aux trois autres.

### Lancement du programme 

Dans un terminal ou l’invité de commande windows, rendez vous dans le repertoire "Code" à l’aide des commandes `cd` et tapez `python3 Affectation_2.0.py`. Vous devriez alors obtenir une liste de commande SQL accompagnée de statistique. Copiez TOUTES les lignes de commandes et collez-les dans la base de données dans l’espace prévu à cet effet.

Vous devez refaire le paramétrage pour chaque fac et relancer le programme pour générer de nouvelles commandes.