import os
import tempfile
from subprocess import check_output
from collections import defaultdict

from django.conf import settings

"""#########PRONONCIATION###########"""
"""Module pour former la prononciation de la phrase sortie par le système"""

"""on cherche la prononciation des mots de la phrase du système"""
def prononciation(phrase_systeme, dictionnaire):
    #on stocke les prononciations pour les réutiliser après
    prononciation_systeme = []
    for mot in phrase_systeme.split(" "): #parcourt la phrase
        for k,v in dictionnaire.items(): #parcourt le dictionnaire
            if mot == k: #si le mot de la phrase est dans les clés (mots) du dictionnaire, on garde sa prononciation
                #print(j,k)
                prononciation_systeme.append(v)
    return prononciation_systeme #retourne une liste

"""on forme la prononciation de la phrase en str"""
def prononciation_to_str(liste_systeme):
    prononciation = ''
    for mot in liste_systeme:
        prononciation+= mot+' '
    return prononciation

"""#########DICTIONNAIRE###########"""
#fonction pour transformer le fichier .dic de sphinx en dictionnaire traitable
#par python
def sphinx_dic(file_dictionary):
    dictionnaire= {} #transformation en dictionnaire

    for line in file_dictionary: #parcourt chaque ligne du dictionnaire sphinx
        liste = []
        if line != '\n': #on retire les lignes vides
            liste = line.split() #on coupe pour obtenir tous les éléments de la ligne
            clef = liste[0] #le premier élément de la ligne est le mot, il sera la clef du dico
            str_pron = "" #contiendra la prononciation du mot
            liste.pop(0) #retire le premier élément de la liste pour ne traiter que la prononciation
            for phon in liste:
                str_pron += phon+' ' #prononciation du mot
            dictionnaire[clef] = str_pron.lstrip("-").rstrip() #on retire l'espace en trop et on ajoute en valeur du dico
    return dictionnaire

"""###################################################################"""
"""découpage du str prononciation avec la fonction de récursion"""
container = [] #contiendra tous les découpages possibles de notre str prononciation

#IANA : variable qui contient le nb maximal de phonemes dans un mot.
#Ce nombre peut etre calcule a partir du dictionnaire, ou bien saisi manuellement.
max_phonemes = 10  # pour notre cas de test

#IANA : fonction qui trouve les mots possibles dans le ditionnaire a partir d'une prononciation
# la fonction retourne la liste vide si le mot n'est pas dans le dictionnaire
def trouver_mots(prononciation) :
	resultat = []
	for k, v in dictionnaire.items():
		if v == prononciation:
			resultat.append(k)
	return resultat

#IANA : fonction qui ajoute un element au debut des listes dans une liste :
# necessaire pour "coller" les 1e elements dans la recursion
# suites contient des decoupages d'une partie d'une chaine
def ajoute(debut, suites) :

	print("Adding " + debut + " to " + str(suites))

	if (not suites) :
		# ici suites == False
		return False

	# ici suites est une liste avec des elements
	for s in suites :
		if (s != False) :
			s.insert(0, debut)

	#print("Resultat : " + str(suites) +"\n")
	return suites

# fonction recursive
# chaine_phonemes est une chaine de phonemes a decouper
# suites est une liste de decoupages, qui peut etre vide
# la fonction retourne une liste des decoupages si le decoupage a ete possible jusqu'au bout de la chaine
# sinon elle retourne false
def decoupe_reste(chaine_phonemes):
	# si la chaine_phonemes est vide, le seul decoupage est le decoupage vide
	if chaine_phonemes == "" :
		#print("Chaine vide restante.")
		return [[]]

	# si la chaine_phonemes contient 1 seul phoneme :
	if len(chaine_phonemes.split(" ")) == 1:
		print("Chaine avec un seul phoneme : " + chaine_phonemes)
		# on verifie si c'est un mot possible :
		mots = trouver_mots(chaine_phonemes)
		decoupages = []
		if (len(mots) > 0) :
			for m in mots :
				print("Mot trouvé : " + m)
			return [mots]
		else:
			print("Pas de mot trouve.")
			return False

	debut = ""	# variable qui contient le debut de la souchaine.
	# On verifiera tous les debuts possibles qui se trouvent dans le dictionnaire.
	# On traite toutes les phonemes :
	ph_count = 0

	suites = []
	debut_possible_trouve = False
	for phoneme in chaine_phonemes.split(" "):
		ph_count += 1 # compteur pour savoir combient de phonemes on a traites depuis le debut de la chaine
		if (ph_count > max_phonemes) :
			break	# sortie de la boucle, parce que si on depasse le nb max de phonemes,
			# nous sommes surs que ce debut de chaine_phonemes ne correspond a aucun mot du dictionnaire
		debut += (" " + phoneme) # le debut de la chaine_phonemes

		debut = debut.strip() # supression d'espaces au debut et a la fin
		#print ("Debut a examiner : " + debut)

		# on verifie si ce debut est dans le dictionnaire
		premier_mots = trouver_mots(debut)
		if len(premier_mots)>0:
			debut_possible_trouve = True
			# nous avons un debut possible
			#print("Mots trouves : " + str(premier_mots))

			reste_de_la_chaine =  chaine_phonemes[len(debut):].strip() #le restant de la chaine apres le debut
			print("Reste de la chaine : " + reste_de_la_chaine)
			# on examine si le reste de la chaine peut etre decoupe a partie du dictionnaire

			for p in premier_mots :
				t = ajoute(p, decoupe_reste(reste_de_la_chaine))
				if t :
					suites.extend(t)
		else:
			print("Pas de mot pour ce debut.")

	#print suites
	if (not debut_possible_trouve) :
		return False
	return suites


dictionnaire_sphinx = open('datasets/small.dic', 'r')
#transformation en objet dictionnaire pour le traitement python
dictionnaire = sphinx_dic(dictionnaire_sphinx)
