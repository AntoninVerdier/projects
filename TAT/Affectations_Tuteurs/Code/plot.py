import matplotlib.pyplot as plt
import settings_pref_params as spp


plt.style.use('fivethirtyeight')

path = spp.path()
params = spp.params()
prefs = spp.prefs()

def plot_scores(affectations_scores, users):

	scores_plot = [affectations_scores[user] for user in users]

	x = [scores_plot.count(i)*100/len(scores_plot) for i in range(5)]
	plt.hist(x)

	print('Pourcentage d\'utilisateur ayant leur premier voeu : ', scores_plot.count(1)*100/len(scores_plot))
	print('Pourcentage d\'utilisateur ayant leur second voeu : ', scores_plot.count(2)*100/len(scores_plot))
	print('Pourcentage d\'utilisateur ayant leur troiseme voeu : ', scores_plot.count(3)*100/len(scores_plot))
	print('Pourcentage d\'utilisateur ayant leur dernier voeu : ', scores_plot.count(4)*100/len(scores_plot))
	print('Pourcentage d\'utilisateur n\'ayant aucun voeu : ', scores_plot.count(params.weight_null)*100/len(scores_plot))

	#plt.xlabel('Users')
	#plt.ylabel('Score')
	#plt.scatter(users, scores_plot)
	#plt.show()