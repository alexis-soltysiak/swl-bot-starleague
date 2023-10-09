import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import os
import warnings
import re
import kaleido
from selenium import webdriver
import time
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)

def testPointSeparation(classement,dfMatch,playerIloc1, playerIloc2):
  #si J1 == J2
  if (classement.iloc[playerIloc1]["points"] == classement.iloc[playerIloc2]["points"]):
    #si ordre bleu rouge
    if len(dfMatch[(dfMatch["Joueur Bleu"] == classement.iloc[playerIloc1]["Pseudo Discord"]) & (dfMatch["Joueur Rouge"] == classement.iloc[playerIloc2]["Pseudo Discord"])]["Vainqueur"]):
      #si vainqueur bleu
      if (dfMatch[(dfMatch["Joueur Bleu"] == classement.iloc[playerIloc1]["Pseudo Discord"]) & (dfMatch["Joueur Rouge"] == classement.iloc[playerIloc2]["Pseudo Discord"])]["Vainqueur"].iloc[0] == "Joueur Bleu"):
        classement.loc[classement['Pseudo Discord'] == classement.iloc[playerIloc1]["Pseudo Discord"], 'pointsSeparation'] += 1
      #si vainqueur rouge
      else :
        classement.loc[classement['Pseudo Discord'] == classement.iloc[playerIloc2]["Pseudo Discord"], 'pointsSeparation'] += 1

    #si ordre rouge bleu
    elif len(dfMatch[(dfMatch["Joueur Bleu"] == classement.iloc[playerIloc2]["Pseudo Discord"]) & (dfMatch["Joueur Rouge"] == classement.iloc[playerIloc1]["Pseudo Discord"])]["Vainqueur"]):
      #si vainqueur bleu
      if (dfMatch[(dfMatch["Joueur Bleu"] == classement.iloc[playerIloc2]["Pseudo Discord"]) & (dfMatch["Joueur Rouge"] == classement.iloc[playerIloc1]["Pseudo Discord"])]["Vainqueur"].iloc[0] == "Joueur Bleu"):
        classement.loc[classement['Pseudo Discord'] == classement.iloc[playerIloc2]["Pseudo Discord"], 'pointsSeparation'] += 1
      #si vainqueur rouge
      else :
        classement.loc[classement['Pseudo Discord'] == classement.iloc[playerIloc1]["Pseudo Discord"], 'pointsSeparation'] += 1

  return classement

def dealWithEqualityPoint(classement,dfMatch):
  classement = testPointSeparation(classement,dfMatch,0, 1)
  classement = testPointSeparation(classement,dfMatch,0, 2)
  classement = testPointSeparation(classement,dfMatch,0, 3)
  classement = testPointSeparation(classement,dfMatch,1, 2)
  classement = testPointSeparation(classement,dfMatch,1, 3)
  classement = testPointSeparation(classement,dfMatch,2, 3)
  return classement


def dealWithSoS(classement):

  for index, row in classement.iterrows():
    sum = 0
    if (classement[classement["Pseudo Discord"]== row["Pseudo Discord"] ]["nbMatchPlayed"].iloc[0] != 0):
      for enemyPlayer in  row["playerPlayed"].split(","):

        #print(classement[classement["Pseudo Discord"]== enemyPlayer ]["points"])
        #print(classement[classement["Pseudo Discord"]== enemyPlayer ]["nbMatchPlayed"])
        sum += classement[classement["Pseudo Discord"]== enemyPlayer ]["points"].iloc[0] / classement[classement["Pseudo Discord"]== enemyPlayer ]["nbMatchPlayed"].iloc[0]
      classement.loc[classement['Pseudo Discord'] == row["Pseudo Discord"], 'SoS'] = round(sum / classement[classement["Pseudo Discord"]== row["Pseudo Discord"] ]["nbMatchPlayed"].iloc[0],2)
    else :
      classement.loc[classement['Pseudo Discord'] == row["Pseudo Discord"], 'SoS'] = sum

  return classement

def figSavingAndShowing(ligue,nomSave,fig):

    # Afficher la figure dans un navigateur et la sauvegarder
    filepath = "Results/"+ligue+"/"+str(nomSave)+".png"
    
    fig.savefig(filepath)
    print(f"done for {filepath}")
    return 



def neon_plot(x, y, ax=None):
    if ax is None:
        ax = plt.gca()
    line, = ax.plot(x, y, lw=1, zorder=6)
    for cont in range(6, 1, -1):
        ax.plot(x, y, lw=cont, color=line.get_color(), zorder=5, alpha=0.05)
    return ax


  
def graphWinLose(dfMatchMerged, listWinLose, ligue):

  data = []
  for winner in listWinLose:

    dfMatchMergedLigue = dfMatchMerged.copy()

    if ligue != "Total":
      dfMatchMergedLigue =  dfMatchMergedLigue[dfMatchMergedLigue["Ligue"] == ligue]

    data.append(len(dfMatchMergedLigue[dfMatchMergedLigue["Vainqueur"] == winner]))


  colors = ['RoyalBlue', 'red', 'LightGray']

  fig, ax = plt.subplots(figsize=(8, 6))  # 800x600 en pixels
  wedges, texts, autotexts = ax.pie(data, labels=listWinLose, colors=colors, 
                                autopct='%1.1f%%', pctdistance=0.35,  # ajustez la valeur de pctdistance
                                startangle=90, wedgeprops=dict(width=0.3, edgecolor='black'))

  # Configuration de la taille et du style du texte
  for t in texts:
    t.set(size=20)
  for t in autotexts:
    t.set(size=20)

  # Titre
  ax.set_title("Win Rate Blue/Red/egalite", size=20)

  return fig


def graphPrObjectives(dfMatchMerged, listObjectives, ligue):

  data = []
  for objective in listObjectives:

    dfMatchMergedLigue = dfMatchMerged.copy()

    if ligue != "Total":
      dfMatchMergedLigue =  dfMatchMergedLigue[dfMatchMergedLigue["Ligue"] == ligue]

    data.append(len(dfMatchMergedLigue[dfMatchMergedLigue["Objectif"] == objective]))

  colors = ['LightCyan', 'LightGoldenRodYellow', 'LightGray','LightGreen', 'LightPink', 'LightSalmon','LightSeaGreen', 'LightSkyBlue']


  
  # Créer le pie chart
  fig, ax = plt.subplots(figsize=(15, 8))  # Ajuster la largeur pour accueillir la légende

  wedges, texts = ax.pie(data, colors=colors, startangle=90, wedgeprops=dict(width=0.3, edgecolor='black'))

  # Retirer les textes
  for t in texts:
      t.set_text("")  # vide les noms

  # Titre
  ax.set_title("Pick Rate Objectives", size=20)

  # Légende agrandie
  legend_labels = ["{} - {:.1f}%".format(obj, perc) for obj, perc in zip(listObjectives, 100.*np.array(data)/sum(data))]
  ax.legend(wedges, legend_labels, title="Objectives", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), prop={'size': 16})
  # Décaler le diagramme circulaire vers la gauche
  ax.set_position([0, 0.1, 0.6, 0.75])
  # Ajustez la position de la légende


    
  return fig



def update_all_results():
    lienMatch = "bdd/match.csv"
    lienList = "bdd/users.csv"
    dfMatch = pd.read_csv(lienMatch,delimiter = ",")
    dfList = pd.read_csv(lienList,delimiter = ",")
    
    # Création des répertoires
    os.makedirs("Results/Total", exist_ok=True)
    os.makedirs("Results/Coruscant", exist_ok=True)
    os.makedirs("Results/Alderaan", exist_ok=True)
    os.makedirs("Results/Tatooine", exist_ok=True)
    os.makedirs("Results/Kessel", exist_ok=True)
    
    dfList = dfList.loc[:, ~dfList.columns.str.contains('^Unnamed')]

    try :
        dfList = dfList.drop(columns=['Prenom Nom'])
        dfList = dfList.drop(columns=['Lien Armé'])
        dfList = dfList.drop(columns=['Column1'])
        dfList = dfList.drop(columns=['mots clés'])
    except :
        pass
    try :
        dfList['SoS'] = 0
        dfList['sumKP'] = 0
        dfList['sumPV'] = 0
        dfList['playerPlayed'] = ""
        dfList['victory'] = 0
        dfList['defeat'] = 0
        dfList['egality'] = 0
        dfList['nbMatchPlayed'] = 0
        dfList['points'] = 0
    except :
        pass
    
    
    for index, row in dfMatch.iterrows():
        Jbleu = row["Joueur Bleu"]
        Jrouge = row["Joueur Rouge"]

        #BLEU GAGNE
        if row["Vainqueur"] == "Joueur Bleu":
            dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'victory'] += 1
            dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'points'] += 3

            dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'defeat'] += 1

        #ROUGE GAGNE
        elif row["Vainqueur"] == "Joueur Rouge":
            dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'victory'] += 1
            dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'points'] += 3

            dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'defeat'] += 1


        else :
            dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'egality'] += 1
            dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'points'] += 1

            dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'egality'] += 1
            dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'points'] += 1

        #KP AND PV
        dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'sumKP'] += row["Kill Point Joueur Bleu (chiffre seulement)"]
        dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'sumPV'] += row["Points de Victoire Joueur Bleu (chiffre seulement)"]
        dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'sumKP'] += row["Kill Point Joueur Rouge (chiffre seulement)"]
        dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'sumPV'] += row["Points de Victoire Joueur Rouge (chiffre seulement)"]


        #LISTPLAYED PLAYED
        if (len(dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'playerPlayed'].iloc[0]) != 0):
            dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'playerPlayed'] += str("," + str(Jrouge))
        else :
            dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'playerPlayed'] += str(str(Jrouge))

        if (len(dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'playerPlayed'].iloc[0]) != 0):
            dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'playerPlayed'] += str("," + str(Jbleu))
        else :
            dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'playerPlayed'] += str(str(Jbleu))


        #NB matchs done
        dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'nbMatchPlayed'] += 1
        dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'nbMatchPlayed'] += 1

        

    ligues = ["Coruscant", "Alderaan", "Tatooine", "Kessel"]

    DfClassementL1 = [
        dfList[(dfList["Ligue"] == "Coruscant") & (dfList["Poule"] == 'A')],
        dfList[(dfList["Ligue"] == "Coruscant") & (dfList["Poule"] == 'B')],
        dfList[(dfList["Ligue"] == "Coruscant") & (dfList["Poule"] == 'C')],
        dfList[(dfList["Ligue"] == "Coruscant") & (dfList["Poule"] == 'D')],
    ]

    DfClassementL2 = [
        dfList[(dfList["Ligue"] == "Alderaan") & (dfList["Poule"] == 'A')],
        dfList[(dfList["Ligue"] == "Alderaan") & (dfList["Poule"] == 'B')],
        dfList[(dfList["Ligue"] == "Alderaan") & (dfList["Poule"] == 'C')],
        dfList[(dfList["Ligue"] == "Alderaan") & (dfList["Poule"] == 'D')],
    ]

    DfClassementL3 = [
        dfList[(dfList["Ligue"] == "Tatooine") & (dfList["Poule"] == 'A')],
        dfList[(dfList["Ligue"] == "Tatooine") & (dfList["Poule"] == 'B')],
        dfList[(dfList["Ligue"] == "Tatooine") & (dfList["Poule"] == 'C')],
        dfList[(dfList["Ligue"] == "Tatooine") & (dfList["Poule"] == 'D')],
    ]

    DfClassementL4 = [
        dfList[(dfList["Ligue"] == "Kessel") & (dfList["Poule"] == 'A')],
        dfList[(dfList["Ligue"] == "Kessel") & (dfList["Poule"] == 'B')],
    ]

    DfClassement = [DfClassementL1,DfClassementL2,DfClassementL3,DfClassementL4]


    f = open("classement.html", "w")

    f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><link rel='stylesheet' href='./Css/classementcss.css'><link rel='icon' href='./Media/get-star-wars-png-pictures-3.png' /><link rel='stylesheet' href='./Css/style.css'></head><body><header><div><div class='gutter'><img src='./images/logo-star-league-s2.svg' alt=''><nav><ul id='navbar'><li><a href='https://www.star-league.fr/classement.html'>Classement</a></li><li><a href='https://www.star-league.fr/index.html'>Global </a></li><li><a href='https://www.star-league.fr/coruscant.html'>Coruscant</a></li><li><a href='https://www.star-league.fr/alderaan.html'>Alderaan</a></li><li><a href='https://www.star-league.fr/tatooine.html'>Tatooine</a></li><li><a href='https://www.star-league.fr/kessel.html'>Kessel</a></li></ul></nav></div></div></header><main class='gutter2'>")

    index = 0
    for classment in DfClassement :

        for count, classement in enumerate(classment):

            #sorting
            classement = classement.sort_values(by='points', ascending=False)
            classement["pointsSeparation"] = classement["points"]

            #Deal with equality
            classement = dealWithEqualityPoint(classement,dfMatch)


            #Deal With SoS
            classement = dealWithSoS(classement)
            #sorting
            classement = classement.sort_values(by=['pointsSeparation', 'SoS', 'sumKP', 'sumPV'], ascending=False)

            if (index == 0):
                dfFinalResults = classement.copy()
                dfFinalResultsHTML = classement.copy()
            else:
                dfFinalResults = pd.concat([dfFinalResults, classement], ignore_index=True)
                dfFinalResultsHTML = pd.concat([dfFinalResultsHTML, classement], ignore_index=True)


            s = pd.Series(["--------","----  ","----------","-----------------------","-----","-----","-----","-----","-----","-----","-----","-----","-----","-----"],index=['Ligue','Poule','Pseudo','Pseudo Discord','victory','defeat','egality','points',"SoS","nbMatchPlayed","Faction","Format","Nombre d'activation","Nombre de points"])

            # Appending empty series to df
            dfFinalResultsHTML.loc[len(dfFinalResultsHTML)] = s

            try :
                classement = classement.drop(columns=["pointsSeparation","mots clés"])
            except :
                pass
 
            #display(classement)

            #classement.to_csv("Results/Total/"+ str(index)+ ".csv",index=False)

            index+=1

    try :
        #Creations nouvelles collones
        dfFinalResultsHTML["Nbre de Pts"] = dfFinalResultsHTML["Nombre de points"]
        dfFinalResultsHTML["Victoires"] = dfFinalResultsHTML["victory"]
        dfFinalResultsHTML["Défaites"] = dfFinalResultsHTML["defeat"]
        dfFinalResultsHTML["Égalités"] = dfFinalResultsHTML["egality"]
        dfFinalResultsHTML["Nbre de Match"] = dfFinalResultsHTML["nbMatchPlayed"]
        dfFinalResultsHTML["Pts Évnmt"] = dfFinalResultsHTML["points"]
        dfFinalResultsHTML["Nbre d'Actis"] = dfFinalResultsHTML["Nombre d'activation"]

        #drop des colonnes inutiles
        dfFinalResultsHTML = dfFinalResultsHTML.drop(columns=["Pseudo","pointsSeparation","mots clés","playerPlayed","sumKP","sumPV"])
        dfFinalResultsHTML = dfFinalResultsHTML.drop(columns=["victory","defeat","egality","nbMatchPlayed","points","Nombre d'activation","Nombre de points"])

        #on choisit les colonnes qu'on garde , dans l'ordre qu'on veut
        dfFinalResultsHTML = dfFinalResultsHTML[["Ligue","Poule","Pseudo Discord","Faction","Format","Nbre de Pts","SoS","Nbre de Match","Nbre d'Actis","Victoires","Défaites","Égalités","Pts Évnmt"]]
    except :
        pass

    """
    f.write(dfFinalResultsHTML.to_html(index=False))
    f.write("</main>")
    """
    f.close()
    
    f = open("classementGeneral.html", "w")

    f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><link rel='stylesheet' href='./Css/classementcss.css'><link rel='icon' href='./Media/get-star-wars-png-pictures-3.png' /><link rel='stylesheet' href='./Css/style.css'></head><body><header><div><div class='gutter'><img src='./images/logo-star-league-s2.svg' alt=''><nav><ul id='navbar'><li><a href='https://www.star-league.fr/classement.html'>Classement</a></li><li><a href='https://www.star-league.fr/index.html'>Global </a></li><li><a href='https://www.star-league.fr/coruscant.html'>Coruscant</a></li><li><a href='https://www.star-league.fr/alderaan.html'>Alderaan</a></li><li><a href='https://www.star-league.fr/tatooine.html'>Tatooine</a></li><li><a href='https://www.star-league.fr/kessel.html'>Kessel</a></li></ul></nav></div></div></header><main class='gutter2'>")

    index = 0

    generalClassement = dfList.copy()
    #sorting
    generalClassement = generalClassement.sort_values(by='points', ascending=False)
    generalClassement["pointsSeparation"] = generalClassement["points"]

    #Deal with equality
    generalClassement = dealWithEqualityPoint(generalClassement,dfMatch)

    #Deal With SoS
    generalClassement = dealWithSoS(generalClassement)
    #sorting
    generalClassement = generalClassement.sort_values(by=['pointsSeparation','SoS','sumKP','sumPV'], ascending=False)

    if (index == 0):
        dfFinalResults = generalClassement.copy()
        dfFinalResultsHTMLGeneral = generalClassement.copy()
    else:
        dfFinalResults = pd.concat([dfFinalResults, generalClassement], ignore_index=True)
        dfFinalResultsHTMLGeneral = pd.concat([dfFinalResultsHTMLGeneral, generalClassement], ignore_index=True)

    s = pd.Series(["--------", "----  ", "----------", "-----------------------", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"], 
                index=['Ligue', 'Poule', 'Pseudo', 'Pseudo Discord', 'victory', 'defeat', 'egality', 'points', "SoS", "nbMatchPlayed", "Faction", "Format", "Nombre d'activation", "Nombre de points"])

    # Adding the series to the DataFrame using loc
    dfFinalResultsHTMLGeneral.loc[len(dfFinalResultsHTMLGeneral)] = s


    try :
        generalClassement = generalClassement.drop(columns=["pointsSeparation","mots clés"])
    except :
        pass

    #display(classement)


    generalClassement.to_csv("Results/Total/"+ str(index)+ ".csv",index=False)

    index+=1

    try :
        #Creations nouvelles collones
        dfFinalResultsHTMLGeneral["Nbre de Pts"] = dfFinalResultsHTMLGeneral["Nombre de points"]
        dfFinalResultsHTMLGeneral["Victoires"] = dfFinalResultsHTMLGeneral["victory"]
        dfFinalResultsHTMLGeneral["Défaites"] = dfFinalResultsHTMLGeneral["defeat"]
        dfFinalResultsHTMLGeneral["Égalités"] = dfFinalResultsHTMLGeneral["egality"]
        dfFinalResultsHTMLGeneral["Nbre de Match"] = dfFinalResultsHTMLGeneral["nbMatchPlayed"]
        dfFinalResultsHTMLGeneral["Pts Évnmt"] = dfFinalResultsHTMLGeneral["points"]
        dfFinalResultsHTMLGeneral["Nbre d'Actis"] = dfFinalResultsHTMLGeneral["Nombre d'activation"]

        #drop des colonnes inutiles
        dfFinalResultsHTMLGeneral = dfFinalResultsHTMLGeneral.drop(columns=["Pseudo","pointsSeparation","mots clés","playerPlayed","sumKP","sumPV"])
        dfFinalResultsHTMLGeneral = dfFinalResultsHTMLGeneral.drop(columns=["victory","defeat","egality","nbMatchPlayed","points","Nombre d'activation","Nombre de points"])

        #on choisit les colonnes qu'on garde , dans l'ordre qu'on veut
        dfFinalResultsHTMLGeneral = dfFinalResultsHTMLGeneral[["Ligue","Poule","Pseudo Discord","Faction","Format","Nbre de Pts","SoS","Nbre de Match","Nbre d'Actis","Victoires","Défaites","Égalités","Pts Évnmt"]]
    except :
        pass

    """
        f.write(dfFinalResultsHTMLGeneral.to_html(index=False))
        f.write("</main>")
    """
    f.close()
    
    generalClassement.to_csv("bdd/classement.csv", index=False)
    
    
    
    
    dfListTmp = dfList.copy()
    dfListTmp["Joueur Bleu"] = dfList["Pseudo Discord"]
    dfMatchMerged = dfMatch.merge(dfListTmp, how='inner', on='Joueur Bleu')
    dfMatchMerged = dfMatchMerged.drop(columns=["Adresse e-mail","Pseudo Discord","Pseudo","victory","defeat","egality",	"points"])

    ####################################################################################
    #WR
    ####################################################################################
    
    #get objective list
    listWinLose = list(dfMatchMerged["Vainqueur"].unique())

    #remove Nan
    listWinLose = [x for x in listWinLose if str(x) != 'nan']

    #name of png and json
    saveName = "WrBlueRed"
    
    ligue = "Total"
    fig = graphWinLose(dfMatchMerged, listWinLose, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Coruscant"
    fig = graphWinLose(dfMatchMerged, listWinLose, ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Alderaan"
    fig = graphWinLose(dfMatchMerged, listWinLose, ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Tatooine"
    fig = graphWinLose(dfMatchMerged, listWinLose, ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Kessel"
    fig = graphWinLose(dfMatchMerged, listWinLose, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    
    ####################################################################################
    #OBJECTIVE
    ####################################################################################
    
    #get objective list
    listObjectives = list(dfMatchMerged["Objectif"].unique())
    #remove Nan
    listObjectives = [x for x in listObjectives if str(x) != 'nan']

    saveName = "PrObjectives"
    
    ligue = "Total"
    fig = graphPrObjectives(dfMatchMerged, listObjectives, ligue)
    figSavingAndShowing(ligue,saveName,fig)


    ligue = "Coruscant"
    fig = graphPrObjectives(dfMatchMerged, listObjectives, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    
    ligue = "Alderaan"
    fig = graphPrObjectives(dfMatchMerged, listObjectives, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    
    ligue = "Coruscant"
    fig = graphPrObjectives(dfMatchMerged, listObjectives, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    
    ligue = "Kessel"
    fig = graphPrObjectives(dfMatchMerged, listObjectives, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Tatooine"
    fig = graphPrObjectives(dfMatchMerged, listObjectives, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    print("ere")

    return
