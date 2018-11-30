import numpy as np
import csv 
import settings_pref_params as spp
import random
import argparse
from scipy.optimize import linear_sum_assignment
import plot

path = spp.path()
params = spp.params()
prefs = spp.prefs()

parser = argparse.ArgumentParser(description='Paramètres pour l\'affectation des tuteurs')

parser.add_argument('--fac', '-f', type=int, 
							help='Choisir la fac sur laquelle lancer l\'algorithme. 1 -> Rangueil, 2 -> Purpan, 4 -> Maraîchers')

args = parser.parse_args()


def get_data_and_split(fac):
	rows = []
	""" Retrieve the data from the csv file and split it by faculties"""
	with open(path.path2csv, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			rows.append(row)
	# Remove header row
	rows = rows[1:len(rows)-1]

	# Remove last empty value on row
	print(len(rows))
	print(rows[0])

	# Sort data by faculty number
	rows_fac = [rows[i] for i in range(len(rows)) if int(rows[i][4]) == fac]

	return rows, rows_fac

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

rows, rows_fac = get_data_and_split(args.fac)
matrix, users, users_choices = preprocess_data(rows, rows_fac, params.liste_matiere_rangs, params.nb_matiere_rangs)
affectations, mean_cost, affectations_scores = compute_affectations(matrix, users, users_choices, params.liste_matiere_rangs, params.nb_matiere_rangs)
plot.plot_scores(affectations_scores, users)


