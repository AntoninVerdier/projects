#!/usr/bin/python
# -*- coding: utf-8 -*-

# Prototype parrainage
#------------------------------#
# Sexe : 0 -> Both, 1 -> Femme, 2 -> Homme
# Tentatives : 0 -> Both, 1 -> Primant, 2-> Doulant, 3 -> Triplant
# Filières : 0-> EIther, 1 -> Médecine, 2 -> Pharmacie, 3 -> Kiné, 4 -> Odonto, 5 -> Maieu

# Score : Filière -> 5, Tentative -> 4, Sexe -> 1
#------------------------------#

# Input fies must be free of accents and all non relevant rows must be removed by hand

import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment
import csv

# Retrieve data
paces = pd.read_csv("pass.csv")
paces = paces.loc[paces["Je souhaite avoir un parrain / une marraine par le biais du Tutorat "] == "Oui, mais je n'ai PAS ENCORE de parrain/marraine"]
paces = paces.loc[paces["Ton type d'inscription"] == "PASS"]
paces_matrix = paces.values

# Clean genders
paces.loc[paces["J'aimerais avoir : "] == 'Un parrain', "J'aimerais avoir : "] = 1
paces.loc[paces["J'aimerais avoir : "] == 'Une marraine', "J'aimerais avoir : "] = 2

# Clean specialties
specialities = ['Medecine', 'Pharmacie', 'Masso-kinesithérapie', 'Odontologie', 'Maieutique (sage-femme)']
for i, (row, idx) in enumerate(zip(paces["Sa filière : "], paces.index)):
	tmp_row = [j+1 for j, s in enumerate(specialities) if s in row]
	if tmp_row: paces.at[idx, "Sa filière : "] = tmp_row

# Clean data for tries
tentatives = ['Primant', 'Doublant', 'Triplant']
for i, (row, idx) in enumerate(zip(paces["Sa tentative :"], paces.index)):
	tmp_row = [j+1 for j, s in enumerate(tentatives) if s in row]
	if tmp_row: paces.at[idx, "Sa tentative :"] = tmp_row

paces["J'aimerais avoir : "] = [[0] if x == "Cela n'a pas d'importance" else x for x in paces["J'aimerais avoir : "]]
paces["Sa filière : "] = [[0] if x == "Cela n'a pas d'importance" else x for x in paces["Sa filière : "]]
paces["Sa tentative :"] = [[0] if x == "Cela n'a pas d'importance" else x for x in paces["Sa tentative :"]]


# Get a dictionnary data_p2 = {id: [tentative, sexe, filière]}

p2 = pd.read_csv("p2.csv",encoding="utf-8")
p2 = p2.loc[p2["Concernant le parrainage :"] == "Je souhaite participer au parrainage, je n'ai PAS ENCORE de fillieuls"]
p2 = p2.loc[p2["Origine"] != ("L.AS")]
p2_matrix = p2.values

# Clean data for genders
p2.loc[p2["Genre"] == 'Homme', "Genre"] = 1
p2.loc[p2["Genre"] == 'Femme', "Genre"] = 2
p2.loc[p2["Genre"] == 'Ne souhaite pas répondre', "Genre"] = 3

# Clean data for tries
p2.loc[p2["Origine"] == 'PASS', "Origine"] = 1
p2.loc[p2["Origine"] == 'PACES doublants/triplants', "Origine"] = 2

# Clean data for specialites
specialities = ['Médecine', 'Pharmacie', 'Kinésithérapie', 'Odontologie', 'Maïeutique']
for i, s in enumerate(specialities): p2.loc[p2["Filière"] == s, "Filière"] = i + 1

# Clean data number of PACES
p2.loc[p2["Combien veux-tu de nouveaux filleuls ?"] == '3 ou -', "Combien veux-tu de nouveaux filleuls ?"] = 1
p2.loc[p2["Combien veux-tu de nouveaux filleuls ?"] == '3 ou +', "Combien veux-tu de nouveaux filleuls ?"] = 2

relevant_pass = paces[["J'aimerais avoir : ", "Sa filière : ", "Sa tentative :"]]
relevant_p2 = p2[["Origine", "Filière", "Genre", "Combien veux-tu de nouveaux filleuls ?"]]

data_pass = relevant_pass.to_numpy()
data_p2 = relevant_p2.to_numpy()

# Create matrix of scores
score_matrix = np.zeros(shape=(len(data_pass), len(data_p2)))
for i, paces in enumerate(data_pass):
	for j, p2 in enumerate(data_p2):
		score = 0

		# Add score for gender
		if paces[0] == p2[1]:
			score = score + 1
		if paces[0] == 0:
			score = score + 0.5

		# Add score for trial
		if paces[2][0] == p2[0] and len(paces[2]) == 1:
			score = score + 4
		elif p2[0] in paces[2]:
			score = score + 2

		# Add score for specialitie
		if paces[1][0] == p2[2] and len(paces[1]) == 1:
			score = score + 5
		elif p2[2] in paces[1]:
			score = score + 2.5

		score_matrix[i][j] = score

# Implement difference of choices
multiple = len(data_pass) // len(data_p2)
left = len(data_pass) % len(data_p2)

# Make the matrix
score_final = score_matrix
for i in range(multiple - 1):
	score_final = np.hstack((score_final, score_matrix))

# Case 1. Number of paces is inferior to 4* number of p2
if multiple < 4:
	score_final = np.hstack((score_final, score_matrix[:,:left]))

# Case 2. Number of paces is superior to 4* number of p2
if multiple >= 4:
	p2_hot = [p2 for p2 in data_p2 if data_p2[p2][3] > 0]

	hot_multiple = (len(data_pass) - 4*len(data_p2))//len(p2_hot)
	left_multiple = (len(data_pass) - 4*len(data_p2))%len(p2_hot)

	score_matrix_hot = score_matrix[:,p2_hot]

	for i in range(hot_multiple):
		score_final = np.hstack((score_final, score_matrix_hot))

	score_final = np.hstack((score_final, score_matrix_hot[:,:left_multiple]))


row_ind, col_ind = linear_sum_assignment(score_final)

id_affectations = [col_ind[i]%len(data_p2) for i in range(len(col_ind))]
rows = []
for i, pm in enumerate(p2_matrix):
	rows.append([pm[1], pm[2]])
	for j, affectation in enumerate(id_affectations):
		if affectation == i:
			rows.append([paces_matrix[j][1], paces_matrix[j][2], paces_matrix[j][3], paces_matrix[j][4]])
	rows.append("")


rows = np.array(rows)
print(rows.shape)

# final_affectations = pd.DataFrame(data=)
with open("affectations{}.csv".format("PASS"), 'w') as f:
	spamwriter = csv.writer(f, delimiter=';', lineterminator='\n')
	spamwriter.writerows(rows)







