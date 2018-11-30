"""
############### Semestre 1 ################
Biomolécules : 101
Génome : 102
Chimie : 103
(M) Histo-BDR: 201
Biocellulaire : 202
(M) Embryo-BDD: 203
(RP) Histo-Embryo: 204
(RP) BDD-BDR: 205
Biophysique: 301
Mathématiques: 401

############### Semestre 2 ################
Physique/Physio: 302
Anatomie: 501
ICM: 601
SP: 701/702
Recherche: 801
Tête/ Cou: 802
PB: 803
Odonto: 804
Pharma: 805
UFP: 806
"""
class path:
	def __init__(self):
		self.path2csv = 'Data/voeux_R.csv'


class params:
	def __init__(self):
		self.nb_matiere_rangs = [19, 18, 19, 10, 12, 11, 20, 20]
		self.nb_matiere_purps = [17, 17, 16, 14, 13, 12, 16, 16]
		self.nb_matiere_maraich = [15, 15, 15, 13, 18, 13, 19, 14]

		self.liste_matiere_purps = [101, 102, 103, 202, 204, 205, 301, 401]
		self.liste_matiere_rangs = [101, 102, 103, 202, 204, 205, 301, 401]
		self.liste_matiere_maraich = [101, 102, 103, 201, 202, 203, 301, 401]
		self.weight_null = 15


class prefs:
	def __init__(self):
		self.rangs = True
		self.purps = False
		self.maraich = False
		self.old_method = False











