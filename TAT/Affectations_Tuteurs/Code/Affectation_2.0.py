import numpy as np
import csv 
import settings_pref_params as spp
import random

from scipy.optimize import linear_sum_assignment

import plot
# import old_method_affectations

path = spp.path()
params = spp.params()
prefs = spp.prefs()

def old_method(rows ,rows_purps, users, users_choices):
	affectations_old_method = [-1]*len(users)
	users_pick = list(users)
	matiere = []
	aff_1 = 0
	aff_2 = 0
	aff_3 = 0
	aff_4 = 0
	aff_0 = 0
	for i, user in enumerate(users):
		user = random.choice(users_pick)
		if 1 in users_choices[user]:
			if affectations_old_method.count(params.liste_matiere_maraich[users_choices[user].index(1)]) < params.nb_matiere_maraich[users_choices[user].index(1)]:
				affectations_old_method[i] = params.liste_matiere_maraich[users_choices[user].index(1)]
				aff_1 = aff_1 + 1
		elif 2 in users_choices[user]:
			if affectations_old_method.count(params.liste_matiere_maraich[users_choices[user].index(2)]) < params.nb_matiere_maraich[users_choices[user].index(2)]:
				affectations_old_method[i] = params.liste_matiere_maraich[users_choices[user].index(2)]
				aff_2 = aff_2 + 1
		elif 3 in users_choices[user]:
			if affectations_old_method.count(params.liste_matiere_maraich[users_choices[user].index(3)]) < params.nb_matiere_maraich[users_choices[user].index(3)]:
				affectations_old_method[i] = params.liste_matiere_maraich[users_choices[user].index(3)]
				aff_3 = aff_3 + 1
		elif 4 in users_choices[user]:
			if affectations_old_method.count(params.liste_matiere_maraich[users_choices[user].index(4)]) < params.nb_matiere_maraich[users_choices[user].index(4)]:
				affectations_old_method[i] = params.liste_matiere_maraich[users_choices[user].index(4)]
				aff_4 = aff_4 + 1
		aff_0 = len(users) - aff_1 - aff_2 - aff_3 -aff_4
		users_pick.remove(user)

	print('Pourcentage d\'utilisateur ayant leur premier voeu : ', aff_1*100/len(users))
	print('Pourcentage d\'utilisateur ayant leur second voeu : ', aff_2*100/len(users))
	print('Pourcentage d\'utilisateur ayant leur troiseme voeu : ', aff_3*100/len(users))
	print('Pourcentage d\'utilisateur ayant leur dernier voeu : ', aff_4*100/len(users))
	print('Pourcentage d\'utilisateur n\'ayant aucun voeu : ', aff_0*100/len(users))

	return affectations_old_method
def get_data_and_split():
	rows = []
	""" Retrieve the data from the csv file and split it by faculties"""
	with open(path.path2csv, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			rows.append(row)
	# Remove header row
	rows = rows[1:len(rows)-1]

	# Remove last empty value on row
	#rows = [rows[i][:-1] for i in range(len(rows))]
	print(len(rows))
	print(rows[0])

	# Sort data by faculty number
	rows_rangs = [rows[i] for i in range(len(rows)) if int(rows[i][4]) == 1]
	rows_purps = [rows[i] for i in range(len(rows)) if int(rows[i][4]) == 2]
	rows_maraich = [rows[i] for i in range(len(rows)) if int(rows[i][4]) == 4]

	return rows, rows_rangs, rows_purps, rows_maraich

def preprocess_data(rows, rows_fac, topic_list, nb_topic):
	# Remove id and fac_number to process
	rows_fac = [rows_fac[i][1:-1] for i in range(len(rows_fac))]

	# Make a list of users's numbers
	users = list(set([rows_fac[i][0] for i in range(len(rows_fac))]))

	# Clean the data by removing people without 4 wishes
	unwanted_users = []
	for user in users:
		# List of one user wishes
		user_voeu = [rows_fac[i] for i in range(len(rows_fac)) if rows_fac[i][0] == user]
		# If the list containing wishes is not 4-wishes long, remove user as it will not be integrated or manual move required
		if len(user_voeu) != 4:
			unwanted_users.append(user)
	
	# Update user list by removing unwanted users
	users = [user for user in users if user not in unwanted_users]

	# Make a dictionnary of user choices ; dict = {user : [matiere1, matiere2, matiere3, matiere4]}
	users_choices = {}
	matrix = {}
	for user in users:
		# Define a list representing scores
		user_choices = [params.weight_null]*len(topic_list)
		for row in rows_fac:
			if int(row[0]) == int(user):
				for i, matiere in enumerate(topic_list):
					if matiere == int(row[2]):
						# Get score of the corresponding topic
						user_choices[i] = int(row[1])
		
		users_choices[user] = user_choices

		# Prepare the data to be processed. Manually modifying the shape.
		user_matrix = []
		for j, nb in enumerate(nb_topic):
			for i in range(nb):
				user_matrix.append(users_choices[user][j])
			matrix[user] = user_matrix							# To keep track, to have interpretable data for debugging

	final_matrix = []
	for user in matrix:
		final_matrix.append(matrix[user])

	return np.array(final_matrix), users, users_choices

def compute_affectations(matrix, users, users_choices, topic_list, nb_topic):
	matrix_matieres = []
	affectations = {}
	affectations_scores = {}
	row_ind, col_ind = linear_sum_assignment(matrix)
	mean_cost = matrix[row_ind, col_ind].sum() / len(users)

	# Generate topic matrix
	for j, nb in enumerate(nb_topic):
		for i in range(nb):
			matrix_matieres.append(topic_list[j])

	# Generate interpretable dictionnary
	for i, user in enumerate(users):
		affectations[user] = matrix_matieres[col_ind[i]]
		# affectations_scores[user] = [users_choices[user][i] for i in range(len(users_choices[user])) if matrix_matieres[col_ind[i]]]
		affectations_scores[user] = users_choices[user][topic_list.index(matrix_matieres[col_ind[i]])]

	return affectations, mean_cost, affectations_scores

rows, rows_rangs, rows_purps, rows_maraich = get_data_and_split()

if prefs.rangs:
	matrix_rangs, users, users_choices = preprocess_data(rows, rows_rangs, params.liste_matiere_rangs, params.nb_matiere_rangs)
	affectations_rangs, mean_cost_rangs, affectations_scores_rangs = compute_affectations(matrix_rangs, users, users_choices, params.liste_matiere_rangs, params.nb_matiere_rangs)
	plot.plot_scores(affectations_scores_rangs, users)
	affectations_old_method = old_method(rows, rows_rangs, users, users_choices)


if prefs.purps:
	matrix_purps, users, users_choices = preprocess_data(rows, rows_purps, params.liste_matiere_purps, params.nb_matiere_purps)
	affectations_purps, mean_cost_purps, affectations_scores_purps = compute_affectations(matrix_purps, users, users_choices, params.liste_matiere_purps, params.nb_matiere_purps)
	plot.plot_scores(affectations_scores_purps, users)
	affectations_old_method = old_method(rows, rows_purps, users, users_choices)


if prefs.maraich:
	matrix_maraich, users, users_choices = preprocess_data(rows, rows_maraich, params.liste_matiere_maraich, params.nb_matiere_maraich)
	affectations_maraich, mean_cost_maraich, affectations_scores_maraich = compute_affectations(matrix_maraich, users, users_choices, params.liste_matiere_maraich, params.nb_matiere_maraich)
	plot.plot_scores(affectations_scores_maraich, users)
	affectations_old_method = old_method(rows, rows_maraich, users, users_choices)


if prefs.old_method:
	matrix_purps, users, users_choices = preprocess_data(rows, rows_purps, params.liste_matiere_purps, params.nb_matiere_purps)
	affectations_old_method = old_method(rows, rows_purps, users, users_choices)

query = ""
print(len(affectations_scores_rangs))
for user in affectations_rangs:
	query = query + "UPDATE `users` SET matiere = {0} WHERE `id` = {1};\n".format(affectations_rangs[user], user)
print(query)






