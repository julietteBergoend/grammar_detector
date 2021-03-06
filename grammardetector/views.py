from django.shortcuts import render
from .models import Phrases, Tags, Mots, Entrees, Prononciations #import des modèles qui nous seront utiles
from django.conf import settings #import de settings car le modèle langagier se trouve dedans
from django.shortcuts import redirect
from spacy import displacy
from django.http import HttpResponse #import des requetes https
from .utils import decoupe_reste, sphinx_dic, prononciation, prononciation_to_str #script externe: forme toutes les phrases possibles d'une prononciation

"""VUES POUR LES LIENS VERS LES DIFFÉRENTES PAGES"""
#ACCUEIL
def accueil(request):
    return render(request, 'grammardetector/accueil.html')

#PAGE D'INFORMATIONS SUR L'APPLI
def helpmodule(request):
    return render(request, 'grammardetector/utilite.html')

"""VUE POUR LE TEMPLATES  DE LA PAGE OUTIL"""
def affiche(request):
    #TABLES DE LA BDD DONT NOUS AVONS BESOIN
    phrases = Phrases.objects
    suite_de_tags = Tags.objects
    suite_de_mots = Mots.objects
    entree_dico = Entrees.objects
    prononciation_dico = Prononciations.objects

    #DICTIONNAIRE SPHINX
    dictionnaire_sphinx_views = open('datasets/frenchWords62K.dic', 'r')
    #transformation en objet dictionnaire pour le traitement python
    dictionnaire_views = sphinx_dic(dictionnaire_sphinx_views)

    ###########################################################
    #TRAITEMENT DE L'ENTRÉE UTILISATEUR POUR L'ANALYSE GRAMMATICALE
    if 'phrasetexte' in request.GET: #phrasetexte est dans <form><textearea>
        #récupère phrase utilisateur:
        compteur_mots = request.GET['phrasetexte']
        #découpage:
        liste_mots = compteur_mots.split()
        #comptage de la fréquence des mots dans la phrase:
        freqs = {}
        for v in liste_mots:
            freqs[v] = liste_mots.count(v) #chaque mot du vocabulaire est associé à la fréquence du mot dans la liste
        ###########################################################
        #TRAITEMENT GRAMMATICAL DE L'ENTRÉE UTILISATEUR
        lang = settings.LANGUAGE_MODELS['fr'] # chargement du modèle (voir setting)s
        #parsing de la phrase:
        parse = lang(compteur_mots)
        liste_mots = [] #récupération des tokens mots pr les afficher dans html
        liste_tokens = [] #récupération des tokens postag pr les afficher dans html
        liste_lemmes = []  #récupération des lemmes
        liste_depedencies = []
        for token in parse:
            liste_mots.append(token.text)
            liste_tokens.append(token.pos_)
            liste_lemmes.append(token.lemma_)
            liste_depedencies.append(token.dep_)
        ###########################################################
        #TRAITEMENT DES SUITES DE TAGS DE LA BDD
        #on convertir les objets Tags en str
        liste_suites = [] #liste qui servira de comparaison
        for st in suite_de_tags.all():
            suite = []
            suite.append(str(st)) #convertir en str sinon il ajoute des objets
            liste_suites.append(suite) #ajout des petites listes dans la grosse liste
        #output = grande liste (liste_suites) de petites listes (suites)
        ###########################################################
        #REFORMATAGE DE L'ENTRÉE UTILISATEUR
        #transformation de la liste de tokens de l'utilisateur au même format que les listes que nous venons de créer
        #liste de la bdd = ['el, el, el'] VS listes de liste_suites = ['el','el','el']
        strtoken = '' #il faut placer nos éléments dans un str pour obtenir ce format
        for i in liste_tokens[0:-1]: #on ne retient pas le dernier car sinon au aurait ['el, el, el, ']
            strtoken+=i+", "
        strtoken2  = strtoken+str(liste_tokens[-1]) #on ajoute enfin le dernier élément
        #reformatage final de la liste de tokens utilisateur:
        liste_utilisateur = []
        liste_utilisateur.append(strtoken2)
        #output = ['el, el, el']
        ###########################################################
        #COMPARAISON DE LA LISTE UTILISATEUR AVEC CELLES DE LA BDD
        liste_answers=[] #va être utilisée dans le html
        for lst in liste_suites:
            if liste_utilisateur == lst: #on compare notre nouvelle liste utilisateur à toutes les listes de la grande liste (bdd)
                liste_answers.append('true')
            elif liste_utilisateur != lst:
                liste_answers.append('false')
        #outpus liste_answer = liste de true et false, ou seulement false
        ############################################################
        #CORRECTION DE LA PHRASE

        #a) Trouver la prononciation de la phrase
        prononciation_systeme = ''
        phrases_possibles = None
        if 'true' in liste_answers:
            print('rien à charger')
        elif 'false' in liste_answers:
            for mot in liste_mots: #parcourt la phrase
                for entry in entree_dico.all(): #parcourt le dictionnaire
                    if mot.lower() == str(entry).lower(): #si le mot de la phrase est dans les clés (mots) du dictionnaire, on garde sa prononciation
                        prononciation_systeme += str(entry) + ' '
                        prononciation_systeme.rstrip()
            print(prononciation_systeme)
            #appel des fonctions dans utils.py
            prononciation_list = prononciation(prononciation_systeme, dictionnaire_views)
            prononciation_finale = prononciation_to_str(prononciation_list)
            print(prononciation_finale)

            #b) Donner toutes les phrases possibles à partir de cette prononciation
            phrases_possibles = decoupe_reste(prononciation_finale)
            #print("DECOUPAGES : ")
            #print(len(phrases_possibles))

            #d) Donner la phrase correcte à l'utilisateur
            phrase_correcte = ''
            correction = []
            for phrase in phrases_possibles:
                #print(phrase)
                str_phrase = ''
                #transformer les listes en phrases:
                for mot in phrase:
                    str_phrase+=mot+' '
                    str_phrase.rstrip()
                #print(str_phrase)
                #parsing spacy
                correction_parse = lang(str_phrase)
                #conversion du parsing en format traitable avec la BDD 'ADJ, V, ..., '
                liste_tokens_correction = ''
                for token in correction_parse:
                    liste_tokens_correction += token.pos_ +", "
                    liste_tokens_correction.rstrip()
                tags_system = liste_tokens_correction[:-2] #on ne prend pas ', ' en trop
                #print(tags_system)
                #on parcourt la bdd
                for lst in suite_de_tags.all():
                    if str(lst) == tags_system:
                        #print(lst, 'ok')
                        correc = str_phrase + ": " + str(lst) #phrase correspondante à la suite de tags
                        correction.append(correc)
            print(correction)

        return render(request, 'grammardetector/outil.html', {'compteur_mots':compteur_mots, 'liste_mots':len(liste_mots),
            'freqs':freqs, 'tokens':liste_utilisateur, 'depedencies':liste_depedencies,'lemmes':liste_lemmes,
            'mots': liste_mots, 'suite_tags_bdd': suite_de_tags, 'answer':liste_answers,
            'phrases_possibles': phrases_possibles, 'correction': correction})
    ###########################################################
    #TRAITEMENT DE L'ENTRÉE UTILISATEUR POUR LA RECHERCHE DE PHRASES PAR NOMBRE DE MOTS
    elif  'phrasenumber' in request.GET:
        nb_utilisateur = request.GET['phrasenumber'] #nombre entré par l'utilisateur
        phrases_nombre_utilisateur = [] #conserve les phrases trouvées
        for attribut in phrases.all(): #parcourt des attributs de la table Phrases
            if int(nb_utilisateur) == int(attribut.nombre_mots):
                phrases_nombre_utilisateur.append(attribut.phrase)
        return render(request, 'grammardetector/outil.html', {'nb_mots_phrase': nb_utilisateur, 'phrases_nombre_utilisateur':phrases_nombre_utilisateur} )
    ###########################################################
    #TRAITEMENT DE L'ENTRÉE UTILISATEUR POUR LA RECHERCHE DE PHRASES PAR TAGS
    elif  'recherchetag' in request.GET:
        tag_utilisateur = request.GET['recherchetag'] #tag sélectionné par l'utilisateur
        tags_utilisateur = []
        phrase_correspondante = []
        for tag, phrase_cor in zip(suite_de_tags.all(), phrases.all()) :
            if str(tag_utilisateur) in tag.suite_tags and tag.id_tags == phrase_cor.id_phrases:
                tags_utilisateur.append(tag.suite_tags)
                phrase_correspondante.append(phrase_cor.phrase)

        return render(request, 'grammardetector/outil.html', {'tag_utilisateur':tag_utilisateur,'tags_utilisateur': tags_utilisateur,
                                    'phrases': phrase_correspondante})


    #renvoi vers la page admin qd on clique sur le bouton BDD
    elif 'admin' in request.GET:
        return render(request, 'http://127.0.0.1:8000/admin/')
    else:
        return render(request, 'grammardetector/outil.html')
