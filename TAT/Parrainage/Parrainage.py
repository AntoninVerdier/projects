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
paces = pd.read_csv("paces.csv")
paces = paces.ix[paces['Je souhaite avoir un parrain / une marraine par le biais du Tutorat '] == 'Oui']
paces = paces.ix[paces['Ta Faculte :'] == 'Purpan']

paces = paces.as_matrix()
paces_matrix = paces

# Get a dictionnary data_paces = {id: [sexe, filieres, tentatives]}
data_paces = {}

for uid in range(len(paces)):
		data_paces[uid] = [paces[uid][7], paces[uid][8], paces[uid][9]]

# Replace Cela n'a pas d'importance by zero
for paces in data_paces:
	for choice in range(3):
		if data_paces[paces][choice] == 'Cela n\'a pas d\'importance':
			data_paces[paces][choice] = 0

# Clean data for gender:
genders = ['Un parrain', 'Une marraine']
for paces in data_paces:
	for i, gender in enumerate(genders):
		if data_paces[paces][0] == gender:
			data_paces[paces][0] = i + 1

# Clean data for specialites
specialities = ['Medecine', 'Pharmacie', 'Masso-kinesitherapie', 'Odontologie', 'Maieutique']
for paces in data_paces:
	if data_paces[paces][1] != 0:
		state = []
		for i, specialitie in enumerate(specialities):
			if specialitie in data_paces[paces][1]:
				state.append(i+1)
		data_paces[paces][1] = state
	else:
		data_paces[paces][1] = [0]

# Clean data for tries
tentatives = ['Primant', 'Doublant', 'Triplant']
for paces in data_paces:
	if data_paces[paces][2] != 0:
		state = []
		for i, tentative in enumerate(tentatives):
			if tentative in data_paces[paces][2]:
				state.append(i+1)
		data_paces[paces][2] = state
	else:
		data_paces[paces][2] = [0]

# Get a dictionnary data_p2 = {id: [tentative, sexe, filière]}
 
p2 = pd.read_csv("P2P.csv").as_matrix()
p2_matrix = p2
data_p2 = {}
for uid in range(len(p2)):
	data_p2[uid] = [p2[uid][7], p2[uid][8], p2[uid][9], p2[uid][11]]

# Clean data for gender:
genders = ['Homme', 'Femme']
for p2 in data_p2:
	for i, gender in enumerate(genders):
		if data_p2[p2][1] == gender:
			data_p2[p2][1] = i + 1

# Clean data for tries
tentatives = ['Primant', 'Doublant', 'Triplant']
for p2 in data_p2:
	for i, tentative in enumerate(tentatives):
			if tentative in str(data_p2[p2][0]):
				data_p2[p2][0] = i + 1

# Clean data for specialites
specialities = ['Medecine', 'Pharmacie', 'Kinesitherapie', 'Odontologie', 'Maieutique']
for p2 in data_p2:
	for i, specialitie in enumerate(specialities):
		if specialitie in str(data_p2[p2][2]):
			data_p2[p2][2] = i

# Clean data number of PACES
options = ['4 ou -', '4 ou + (une veritable papa/maman poule )', '4 ou +']
for p2 in data_p2:
	for i, option in enumerate(options):
		if option in str(data_p2[p2][3]):
			data_p2[p2][3] = i 


# Create matrix of scores
score_matrix = np.zeros(shape=(len(data_paces), len(data_p2)))
for paces in data_paces:

	for p2 in data_p2:
		score = 0

		# Add score for gender
		if data_paces[paces][0] == data_p2[p2][1]:
			score = score + 1
		if data_paces[paces][0] == 0:
			score = score + 0.5

		# Add score for trial
		if data_paces[paces][2][0] == data_p2[p2][0] and len(data_paces[paces][2]) == 1:
			score = score + 4
		elif data_p2[p2][0] in data_paces[paces][2]:
			score = score + 2

		# Add score for specialitie
		if data_paces[paces][1][0] == data_p2[p2][2] and len(data_paces[paces][1]) == 1:
			score = score + 5
		elif data_p2[p2][2] in data_paces[paces][1]:
			score = score + 2.5

		score_matrix[paces][p2] = score

# Implement difference of choices 
multiple = len(data_paces) // len(data_p2)
left = len(data_paces) % len(data_p2)

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

	hot_multiple = (len(data_paces) - 4*len(data_p2))//len(p2_hot)
	left_multiple = (len(data_paces) - 4*len(data_p2))%len(p2_hot)

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
			rows.append([paces_matrix[j][1], paces_matrix[j][2], paces_matrix[j][5], paces_matrix[j][6]])


rows = np.array(rows)
print(rows.shape)

# final_affectations = pd.DataFrame(data=)
with open("affectations{}.csv".format("Purpan"), 'w') as f:
	spamwriter = csv.writer(f, delimiter=' ')
	spamwriter.writerows(rows)







