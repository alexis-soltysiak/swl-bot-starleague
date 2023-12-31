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
import mplcyberpunk


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
  plt.style.use("cyberpunk")
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
  ax.set_title("Win Rate egalite", size=20)
  mplcyberpunk.add_glow_effects()
  
  return fig





def graphPrObjectives(dfMatchMerged, listObjectives, ligue):
  plt.style.use("cyberpunk")
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

  mplcyberpunk.add_glow_effects()
  return fig



def graphPrDeploiement(dfMatchMerged, listDeployement, ligue):

  plt.style.use("cyberpunk")
  data = []
  for deployement in listDeployement:

    dfMatchMergedLigue = dfMatchMerged.copy()

    if ligue != "Total":
      dfMatchMergedLigue =  dfMatchMergedLigue[dfMatchMergedLigue["Ligue"] == ligue]

    data.append(len(dfMatchMergedLigue[dfMatchMergedLigue["Déploiement"] == deployement]))

  colors = ['LightCyan', 'LightGoldenRodYellow', 'LightGray','LightGreen', 'LightPink', 'LightSalmon','LightSeaGreen', 'LightSkyBlue']

  # Créer le pie chart
  fig, ax = plt.subplots(figsize=(15, 8))  # Ajuster la largeur pour accueillir la légende

  wedges, texts = ax.pie(data, colors=colors, startangle=90, wedgeprops=dict(width=0.3, edgecolor='black'))

  # Retirer les textes
  for t in texts:
      t.set_text("")  # vide les noms

  # Titre
  ax.set_title("Pick Rate Deployement", size=20)

  # Légende agrandie
  legend_labels = ["{} - {:.1f}%".format(obj, perc) for obj, perc in zip(listDeployement, 100.*np.array(data)/sum(data))]
  ax.legend(wedges, legend_labels, title="Deployement", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), prop={'size': 16})
  # Décaler le diagramme circulaire vers la gauche
  ax.set_position([0, 0.1, 0.6, 0.75])
  
  mplcyberpunk.add_glow_effects()  
  return fig



def graphPCondition(dfMatchMerged, listCondition, ligue):

  plt.style.use("cyberpunk")
  data = []
  for condition in listCondition:

    dfMatchMergedLigue = dfMatchMerged.copy()

    if ligue != "Total":
      dfMatchMergedLigue =  dfMatchMergedLigue[dfMatchMergedLigue["Ligue"] == ligue]

    data.append(len(dfMatchMergedLigue[dfMatchMergedLigue["Condition"] == condition]))

  colors = ['LightCyan', 'LightGoldenRodYellow', 'LightGray','LightGreen', 'LightPink', 'LightSalmon','LightSeaGreen', 'LightSkyBlue']

  # Créer le pie chart
  fig, ax = plt.subplots(figsize=(15, 8))  # Ajuster la largeur pour accueillir la légende

  wedges, texts = ax.pie(data, colors=colors, startangle=90, wedgeprops=dict(width=0.3, edgecolor='black'))

  # Retirer les textes
  for t in texts:
      t.set_text("")  # vide les noms

  # Titre
  ax.set_title("Pick Rate Condition", size=20)

  # Légende agrandie
  legend_labels = ["{} - {:.1f}%".format(obj, perc) for obj, perc in zip(listCondition, 100.*np.array(data)/sum(data))]
  ax.legend(wedges, legend_labels, title="Condition", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), prop={'size': 16})
  # Décaler le diagramme circulaire vers la gauche
  ax.set_position([0, 0.1, 0.6, 0.75])
  
  mplcyberpunk.add_glow_effects()
  return fig





def calculationWRPerFactionPerFormat(dfFinalResults,ligue):

  plt.style.use("cyberpunk")
  dfFinalResultWR = dfFinalResults.copy()
  if ligue != "Total":
    dfFinalResultWR =  dfFinalResultWR[dfFinalResultWR["Ligue"] == ligue]

  factionsLabels = dfFinalResultWR["Faction"].unique()

  factionWRGlobal = []
  factionWRStandart = []
  factionWRBi = []

  for faction in factionsLabels :
    dfTMP = dfFinalResultWR[dfFinalResultWR['Faction'] == faction]
    
    denominator = dfTMP["victory"].sum() + dfTMP["defeat"].sum()
    if denominator != 0:
        factionWRGlobal.append(100 * round(dfTMP["victory"].sum() / denominator, 3))
    else:
        factionWRGlobal.append(0)  # ou toute autre valeur par défaut ou traitement d'erreur

    dfTMP = dfFinalResultWR[dfFinalResultWR['Faction'] == faction]

    dfTMP = dfTMP[dfTMP["Format"] == "Standard"]
    denominator = dfTMP["victory"].sum() + dfTMP["defeat"].sum()
    if denominator != 0:
        factionWRStandart.append(100 * round(dfTMP["victory"].sum() / denominator, 3))
    else:
        factionWRStandart.append(0)  # ou toute autre valeur par défaut ou traitement d'erreur

    dfTMP = dfFinalResultWR[dfFinalResultWR['Faction'] == faction]
    dfTMP = dfTMP[dfTMP["Format"] != "Standard"]
    denominator = dfTMP["victory"].sum() + dfTMP["defeat"].sum()
    if denominator != 0:
        factionWRBi.append(100 * round(dfTMP["victory"].sum() / denominator, 3))
    else:
        factionWRBi.append(0)  # ou toute autre valeur par défaut ou traitement d'erreur



  zipped_lists = zip(factionWRGlobal, factionsLabels,factionWRStandart,factionWRBi)
  sorted_pairs = sorted(zipped_lists,reverse = True)
  tuples = zip(*sorted_pairs)
  factionWRGlobal, factionsLabels,factionWRStandart,factionWRBi = [ list(tuple) for tuple in  tuples]


  barWidth = 0.25
  r1 = np.arange(len(factionWRGlobal))
  r2 = [x + barWidth for x in r1]
  r3 = [x + barWidth for x in r2]

  fig, ax = plt.subplots(figsize=(10, 6))

  # Création des barres
  ax.bar(r1, factionWRGlobal, width=barWidth, label='Global')
  ax.bar(r2, factionWRStandart, width=barWidth, label='Standard')
  ax.bar(r3, factionWRBi, width=barWidth, label='Battle Force')

  # Ajout des labels, titres, etc.
  ax.set_xlabel('Factions', fontweight='bold')
  ax.set_xticks([r + barWidth for r in range(len(factionWRGlobal))])
  ax.set_xticklabels(factionsLabels)

  # Ajout des pourcentages sur les barres
  for i in range(len(r1)):
      ax.text(r1[i], factionWRGlobal[i] + 1, f"{factionWRGlobal[i]:.0f}%", ha='center')
      ax.text(r2[i], factionWRStandart[i] + 1, f"{factionWRStandart[i]:.0f}%", ha='center')
      ax.text(r3[i], factionWRBi[i] + 1, f"{factionWRBi[i]:.0f}%", ha='center')

  # Lignes et zones colorées
  ax.axhline(y=50, color='grey', linestyle='--', linewidth=0.5)
  ax.axhspan(50, 100, facecolor='green', alpha=0.1)
  ax.axhspan(0, 50, facecolor='red', alpha=0.1)

  # Configuration de l'axe des y pour les pourcentages
  ax.set_yticks([10, 20, 30, 40, 50, 60, 70, 80, 90])
  ax.set_yticklabels(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%"])

  # Légende
  ax.legend()
  mplcyberpunk.add_glow_effects()
  return fig


def calculationBid(dfFinalResults,ligue):

  plt.style.use("cyberpunk")
  dfFinalResultWR = dfFinalResults.copy()
  

  if ligue != "Total":
    dfFinalResultWR =  dfFinalResultWR[dfFinalResultWR["Ligue"] == ligue]

  dfFinalResultWR["bid"] = 800 - dfFinalResultWR["Nombre de points"]
  bidMean = round(dfFinalResultWR["bid"].mean(),2)
  

  # Initialisation de la figure et de l'axe
  fig, ax = plt.subplots(figsize=(10,3))  # dimensions 300x300 pixels

  # Masquer les axes
  ax.axis('off')

  # Afficher le titre "Bid Moyen" en bas de la valeur
  ax.text(0.5, 0.8, "Bid Moyen", ha='center', va='center', fontsize=20, transform=ax.transAxes)

  # Afficher la valeur de bidMean au centre de l'axe
  ax.text(0.5, 0.3, str(bidMean), ha='center', va='center', fontsize=30, transform=ax.transAxes)

  plt.tight_layout()
  mplcyberpunk.add_glow_effects()
  return fig



def calculatScatterForKP(dfMatchMerged,ligue):

  dfMatchMergedHistogramKp = dfMatchMerged.copy()

  if ligue != "Total":
    dfMatchMergedHistogramKp =  dfMatchMergedHistogramKp[dfMatchMergedHistogramKp["Ligue"] == ligue]

  listAppendKP =[]

  for i in range (0,800,100):
    listAppendKP.append(len(dfMatchMergedHistogramKp[(dfMatchMergedHistogramKp['Kill Point Joueur Bleu (chiffre seulement)']>=i) & (dfMatchMergedHistogramKp['Kill Point Joueur Bleu (chiffre seulement)']< i+100)])\
                      + len(dfMatchMergedHistogramKp[(dfMatchMergedHistogramKp['Kill Point Joueur Rouge (chiffre seulement)']>=i) & (dfMatchMergedHistogramKp['Kill Point Joueur Rouge (chiffre seulement)']< i+100)]))


  x = ['[0-100]','[100-200]','[200-300]', '[300-400]', '[400-500]', '[500-600]', '[600-700]', '[700-800]']
  y = listAppendKP
  plt.style.use("cyberpunk")

  # Création du graphique
  fig, ax = plt.subplots(figsize=(10, 5))
  # Ajout des données
  ax.plot(x, y, '-og', linewidth=5, markersize=10, markeredgewidth=2, color="green")

  # Mise à jour des titres et des étiquettes des axes
  ax.set_title("KP repartition")
  ax.set_xlabel("Range of KP")
  ax.set_ylabel("N")

  # Mise à jour des couleurs d'arrière-plan
  ax.set_facecolor("none")
  fig.patch.set_facecolor("none")
  mplcyberpunk.add_glow_effects()
  return fig

def calculatScatterForKV(dfMatchMerged,ligue):

  dfMatchMergedHistogramKv = dfMatchMerged.copy()

  if ligue != "Total":
    dfMatchMergedHistogramKv =  dfMatchMergedHistogramKv[dfMatchMergedHistogramKv["Ligue"] == ligue]

  listAppendKV =[]

  for i in range (0,11,1):
    listAppendKV.append(len(dfMatchMergedHistogramKv[(dfMatchMergedHistogramKv['Points de Victoire Joueur Bleu (chiffre seulement)']==i)])\
                      + len(dfMatchMergedHistogramKv[(dfMatchMergedHistogramKv['Points de Victoire Joueur Rouge (chiffre seulement)']==i)]))


  x = ['{0}','{1}','{2}', '{3}', '{4}', '{5}', '{6}', '{7}','{8}','{9}','{10}']
  y = listAppendKV
  plt.style.use("cyberpunk")

  # Création du graphique
  fig, ax = plt.subplots(figsize=(10, 5))

  # Ajout des données
  ax.plot(x, y, '-og', linewidth=5, markersize=10, markeredgewidth=2, color="yellow")

  # Mise à jour des titres et des étiquettes des axes
  ax.set_title("VP repartition")
  ax.set_xlabel("Range of VP")
  ax.set_ylabel("N")

  # Mise à jour des couleurs d'arrière-plan
  ax.set_facecolor("none")
  fig.patch.set_facecolor("none")
  mplcyberpunk.add_glow_effects()
  return fig



# Génération de nuances pour chaque couleur de faction
def generate_shades(color, n):
    """Génère n nuances d'une couleur donnée."""
    shades = []
    for i in range(n):
        shades.append([(c * (1 - 0.2*(i/n))) for c in color])
    return shades


def calculationFactionFormat(dfList, ligue):
  dfListFaction = dfList.copy()

  if ligue != "Total":
      dfListFaction = dfListFaction[dfListFaction["Ligue"] == ligue]

  # Pour le donut extérieur, associons chaque format à une faction et comptons les occurrences
  format_counts = dfListFaction.groupby(['Faction', 'Format']).size()
  format_labels = [f"{index[0]}_{index[1]}" for index in format_counts.index]
  format_sizes = format_counts.values

  # Pour le donut intérieur, comptez combien de fois chaque faction apparaît
  faction_sizes = format_counts.groupby(level=0).sum()

  # Couleurs pour les factions
  faction_colors = plt.cm.Paired(range(len(faction_sizes)))

  # Mapper chaque format à une nuance de la couleur de sa faction
  format_colors = []
  for index, size in format_counts.items():

      faction, fmt = index
      faction_color = faction_colors[np.where(faction_sizes.index == faction)[0][0]]
      format_colors.append(generate_shades(faction_color, 1)[0])

  plt.style.use("cyberpunk")
  fig, ax = plt.subplots(figsize=(10, 10))

  # Donut intérieur (Factions)
  wedges1, texts1 = ax.pie(faction_sizes, labels=faction_sizes.index, startangle=90, wedgeprops=dict(width=0.3), colors=faction_colors, labeldistance=0.25)

  # Donut extérieur (Formats)
  wedges2, texts2 = ax.pie(format_sizes, labels=format_labels, startangle=90, wedgeprops=dict(width=0.3), radius=0.75, colors=format_colors, labeldistance=1.3)

  # Ajouter une légende pour la faction
  ax.legend(wedges1, faction_sizes.index, title="Factions", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

  # Augmenter la taille du texte
  for text in texts1 + texts2:
      text.set(size=12)

  mplcyberpunk.add_glow_effects()
  return fig


  
def update_tree():
    lienMatch = "bdd/match.csv"
    lienList = "bdd/users.csv"
    dfMatch = pd.read_csv(lienMatch,delimiter = ",")
    dfList = pd.read_csv(lienList,delimiter = ",")
    
    dfMatch = dfMatch[dfMatch["Phase"] != "Poule"]
        
    correspondance_pseudo_poule = dict(zip(dfList['Pseudo Discord'], dfList['Ligue']))
    correspondance_pseudo_poule2 = dict(zip(dfList['Pseudo'], dfList['Ligue']))

    def obtenir_poule(pseudo):
        poule  = correspondance_pseudo_poule.get(pseudo, '')
        if poule:
          return poule
        else: 
          return correspondance_pseudo_poule2.get(pseudo, '')
      
        # Modifier la colonne "Vainqueur" pour obtenir le pseudo du joueur gagnant
    dfMatch['Vainqueur'] = dfMatch.apply(lambda row: row['Joueur Bleu'] if row['Vainqueur'] == 'Joueur Bleu' else row['Joueur Rouge'], axis=1)
    
        # Créer une nouvelle colonne 'Ligue' dans le DataFrame et l'initialiser à None
    dfMatch['Ligue'] = None

    # Utiliser une boucle pour itérer sur les lignes et appliquer obtenir_poule
    for index, row in dfMatch.iterrows():
        joueur_bleu = row['Joueur Bleu']
        ligue = obtenir_poule(joueur_bleu)
        dfMatch.at[index, 'Ligue'] = ligue

      
    # Sélectionner les colonnes requises pour le ClassementTree et les enregistrer dans un nouveau fichier CSV
    dfMatch[['Phase', 'Ligue', 'Joueur Bleu', 'Joueur Rouge', 'Vainqueur']].to_csv("bdd/classementTree.csv", index=False)

    return 
    
  
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


    
    dfMatch = dfMatch[dfMatch["Phase"] == "Poule"]
    
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
        dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'sumKP'] += int(row["Kill Point Joueur Bleu (chiffre seulement)"])
        dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'sumPV'] += int(row["Points de Victoire Joueur Bleu (chiffre seulement)"])
        dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'sumKP'] += int(row["Kill Point Joueur Rouge (chiffre seulement)"])
        dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'sumPV'] += int(row["Points de Victoire Joueur Rouge (chiffre seulement)"])

        
        try : 
          #LISTPLAYED PLAYED
          if (len(dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'playerPlayed'].iloc[0]) != 0):
              dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'playerPlayed'] += str("," + str(Jrouge))
          else :
              dfList.loc[dfList['Pseudo Discord'] == Jbleu, 'playerPlayed'] += str(str(Jrouge))

          if (len(dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'playerPlayed'].iloc[0]) != 0):
              dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'playerPlayed'] += str("," + str(Jbleu))
          else :
              dfList.loc[dfList['Pseudo Discord'] == Jrouge, 'playerPlayed'] += str(str(Jbleu))
        except : 
          print(f"Error with  {Jbleu} et {Jrouge}")
          return False

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
    
    ####################################################################################
    #DEPLOYEMENT
    ####################################################################################
    
    #get objective list
    listDeployement = list(dfMatchMerged["Déploiement"].unique())

    #remove Nan
    listDeployement = [x for x in listDeployement if str(x) != 'nan']

    #name of png and json
    saveName = "PrDeploiement"
    
    ligue = "Total"
    fig = graphPrDeploiement(dfMatchMerged, listDeployement, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Coruscant"
    fig = graphPrDeploiement(dfMatchMerged, listDeployement, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Alderaan"
    fig = graphPrDeploiement(dfMatchMerged, listDeployement, ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Tatooine"
    fig = graphPrDeploiement(dfMatchMerged, listDeployement, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Kessel"
    fig = graphPrDeploiement(dfMatchMerged, listDeployement, ligue)
    figSavingAndShowing(ligue,saveName,fig)

    
    ####################################################################################
    #CONDITION
    ####################################################################################

    #get CONDITION list
    listCondition = list(dfMatchMerged["Condition"].unique())

    #remove Nan
    listCondition = [x for x in listCondition if str(x) != 'nan']

    #name of png and json
    saveName = "PrCondition"

    ligue = "Total"
    fig = graphPCondition(dfMatchMerged, listCondition, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Coruscant"
    fig = graphPCondition(dfMatchMerged, listCondition, ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Alderaan"
    fig = graphPCondition(dfMatchMerged, listCondition, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Tatooine"
    fig = graphPCondition(dfMatchMerged, listCondition, ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Kessel"
    fig = graphPCondition(dfMatchMerged, listCondition, ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    """
    ####################################################################################
    #FORMAT WR
    ####################################################################################

    saveName = "FactionFormat"
    
    ligue = "Total"
    fig = calculationFactionFormat(dfList,ligue,dfFinalResults)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Coruscant"
    fig = calculationFactionFormat(dfList,ligue,dfFinalResults)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Alderaan"
    fig = calculationFactionFormat(dfList,ligue,dfFinalResults)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Tatooine"
    fig = calculationFactionFormat(dfList,ligue,dfFinalResults)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Kessel"
    fig = calculationFactionFormat(dfList,ligue,dfFinalResults)
    figSavingAndShowing(ligue,saveName,fig)

    ####################################################################################
    #FORMAT WRperFaction
    ####################################################################################

    saveName = "WRPerFactionPerFormat"
    
    
    ligue = "Total"
    fig = calculationWRPerFactionPerFormat(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Coruscant"
    fig = calculationWRPerFactionPerFormat(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Alderaan"
    fig = calculationWRPerFactionPerFormat(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Tatooine"
    fig = calculationWRPerFactionPerFormat(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Kessel"
    fig = calculationWRPerFactionPerFormat(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    """
    
    ####################################################################################
    #meanbid
    ####################################################################################
    
    saveName = "meanBid"
    
    ligue = "Total"
    fig = calculationBid(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Coruscant"
    fig = calculationBid(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Alderaan"
    fig = calculationBid(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Tatooine"
    fig = calculationBid(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Kessel"
    fig = calculationBid(dfFinalResults,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
        
    ####################################################################################
    #KP
    ####################################################################################
    saveName = "HistogramKP"
    
    ligue = "Total"
    fig = calculatScatterForKP(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Coruscant"
    fig = calculatScatterForKP(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Alderaan"
    fig = calculatScatterForKP(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)


    ligue = "Tatooine"
    fig = calculatScatterForKP(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Kessel"
    fig = calculatScatterForKP(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ####################################################################################
    #histo KV
    ####################################################################################
    
    saveName = "HistogramKV"
    
    ligue = "Total"
    fig = calculatScatterForKV(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Coruscant"
    fig = calculatScatterForKV(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Alderaan"
    fig = calculatScatterForKV(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Tatooine"
    fig = calculatScatterForKV(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Kessel"
    fig = calculatScatterForKV(dfMatchMerged,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
        
    ####################################################################################
    #Faction Format
    ####################################################################################
    
    saveName = "FactionFormat"
    
    ligue = "Total"
    fig = calculationFactionFormat(dfList,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    ligue = "Coruscant"
    fig = calculationFactionFormat(dfList,ligue)
    figSavingAndShowing(ligue,saveName,fig)


    ligue = "Alderaan"
    fig = calculationFactionFormat(dfList,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Tatooine"
    fig = calculationFactionFormat(dfList,ligue)
    figSavingAndShowing(ligue,saveName,fig)

    ligue = "Kessel"
    fig = calculationFactionFormat(dfList,ligue)
    figSavingAndShowing(ligue,saveName,fig)
    
    return True



def find_late_guys():
  
    

  # Lire le fichier CSV
  df = pd.read_csv('bdd/classement.csv')

  # Trouver le plus petit nombre de matchs joués
  min_matches = df['nbMatchPlayed'].min()

  # Filtrer la DataFrame pour obtenir seulement les lignes avec le plus petit nombre de matchs joués
  filtered_df = df[df['nbMatchPlayed'] == min_matches]

  # Si nous avons moins de 5 joueurs avec le minimum de matchs joués, nous incluons aussi ceux avec le deuxième minimum
  if len(filtered_df) < 5:
      second_min_matches = df[df['nbMatchPlayed'] > min_matches]['nbMatchPlayed'].min()
      second_filtered_df = df[df['nbMatchPlayed'] == second_min_matches]
      filtered_df = pd.concat([filtered_df, second_filtered_df])

  # Récupérer la liste des pseudos
  pseudos = filtered_df['Pseudo Discord'].tolist()
  

  return pseudos
  
  
def calculation_of_the_number_of_match():
  
  # Lire le fichier CSV
  df = pd.read_csv('bdd/classement.csv')
 # Définir l'ordre des ligues
  ligue_order = ['Coruscant', 'Alderaan', 'Tatooine', 'Kessel']

  # Transformer la colonne 'Ligue' en une catégorie ordonnée
  df['Ligue'] = pd.Categorical(df['Ligue'], categories=ligue_order, ordered=True)

  # Grouper par Ligue et Poule puis sommer le nbMatchPlayed
  grouped = df.groupby(['Ligue', 'Poule']).nbMatchPlayed.sum().reset_index()

  # Diviser la somme par 2 pour obtenir le nombre réel de matchs
  grouped['nbMatchPlayed'] = grouped['nbMatchPlayed'] / 2

  # Trier par 'Ligue' (dans l'ordre défini par la catégorie)
  grouped = grouped.sort_values(by=['Ligue', 'Poule'])
  grouped = grouped[~((grouped['Ligue'] == 'Kessel') & (grouped['Poule'] == 'D'))]


  result = grouped.to_dict('records')

  return result

def get_player_matches(player_name):
    # Lire le fichier CSV
    df = pd.read_csv("bdd/match.csv")

  

    
      # Créer la colonne 'awin'
    df['awin'] = df.apply(lambda row: (row['Vainqueur'] == "Joueur Bleu" and row['Joueur Bleu'] == str(player_name)) or 
                                      (row['Vainqueur'] == "Joueur Rouge" and row['Joueur Rouge'] == str(player_name)), axis=1)

  
      
    df = df.rename(columns={"Points de Victoire Joueur Bleu (chiffre seulement)": "PV Bleu"})
    df = df.rename(columns={"Points de Victoire Joueur Rouge (chiffre seulement)": "PV Rouge"})
    df = df.rename(columns={"Kill Point Joueur Bleu (chiffre seulement)": "KP Bleu"})
    df = df.rename(columns={"Kill Point Joueur Rouge (chiffre seulement)": "KP Rouge"})
 
    # Convertir les colonnes en chaînes de caractères
    columns_to_convert = ["PV Bleu", "PV Rouge", "KP Bleu", "KP Rouge"]
    for col in columns_to_convert:
      df[col] = df[col].astype(str)
        
    # Filtrer les lignes où le joueur est présent
    matches = df.loc[(df['Joueur Bleu'] == str(player_name)) | (df['Joueur Rouge'] == str(player_name))]

  
    # Convertir le DataFrame filtré en une liste de dictionnaires
    result = matches.to_dict('records')
    
    return result
  
def create_full_classement():
  
  dfMatch = pd.read_csv("bdd/match.csv")
  dfList = pd.read_csv("bdd/users.csv")
  
  dfMatch= dfMatch[dfMatch["Phase"] == "Poule"]
  
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




  classement = dfList.copy()

  #sorting
  classement = classement.sort_values(by='points', ascending=False)
  classement["pointsSeparation"] = classement["points"]

  #Deal with equality
  classement = dealWithEqualityPoint(classement,dfMatch)


  #Deal With SoS
  classement = dealWithSoS(classement)
  #sorting
  classement = classement.sort_values(by=['pointsSeparation','SoS','sumKP','sumPV'], ascending=False)


  dfFinalResults = classement.copy()
  dfFinalResultsHTML = classement.copy()

  s = pd.Series(["--------","----  ","----------","-----------------------","-----","-----","-----","-----","-----","-----","-----","-----","-----","-----"],index=['Ligue','Poule','Pseudo','Pseudo Discord','victory','defeat','egality','points',"SoS","nbMatchPlayed","Faction","Format","Nombre d'activation","Nombre de points"])

  # Appending empty series to df
  dfFinalResultsHTML = pd.concat([dfFinalResultsHTML, s], ignore_index=True)

  try :
      classement = classement.drop(columns=["pointsSeparation","mots clés"])
  except :
    pass

  #display(classement)


  classement.to_csv("bdd/classementgeneral.csv",index=False)
  
  return 

