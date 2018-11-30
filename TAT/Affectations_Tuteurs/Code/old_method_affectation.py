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
			if affectations_old_method.count(params.liste_matiere_purps[users_choices[user].index(1)]) < params.nb_matiere_purps[users_choices[user].index(1)]:
				affectations_old_method[i] = params.liste_matiere_purps[users_choices[user].index(1)]
				aff_1 = aff_1 + 1
		elif 2 in users_choices[user]:
			if affectations_old_method.count(params.liste_matiere_purps[users_choices[user].index(2)]) < params.nb_matiere_purps[users_choices[user].index(2)]:
				affectations_old_method[i] = params.liste_matiere_purps[users_choices[user].index(2)]
				aff_2 = aff_2 + 1
		elif 3 in users_choices[user]:
			if affectations_old_method.count(params.liste_matiere_purps[users_choices[user].index(3)]) < params.nb_matiere_purps[users_choices[user].index(3)]:
				affectations_old_method[i] = params.liste_matiere_purps[users_choices[user].index(3)]
				aff_3 = aff_3 + 1
		elif 4 in users_choices[user]:
			if affectations_old_method.count(params.liste_matiere_purps[users_choices[user].index(4)]) < params.nb_matiere_purps[users_choices[user].index(4)]:
				affectations_old_method[i] = params.liste_matiere_purps[users_choices[user].index(4)]
				aff_4 = aff_4 + 1
		aff_0 = len(users) - aff_1 - aff_2 - aff_3 -aff_4
		users_pick.remove(user)

	print('Pourcentage d\'utilisateur ayant leur premier voeu : ', aff_1*100/len(users))
	print('Pourcentage d\'utilisateur ayant leur second voeu : ', aff_2*100/len(users))
	print('Pourcentage d\'utilisateur ayant leur troiseme voeu : ', aff_3*100/len(users))
	print('Pourcentage d\'utilisateur ayant leur dernier voeu : ', aff_4*100/len(users))
	print('Pourcentage d\'utilisateur n\'ayant aucun voeu : ', aff_0*100/len(users))

	return affectations_old_method
