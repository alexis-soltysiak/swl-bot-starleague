# Importing Some stuff for our bot
from typing import Any, Optional
import discord
from discord.ext import commands
import os
from time import sleep
import logging
from discord import Embed, SelectMenu, SelectOption, Button, ButtonStyle,  Interaction
from datetime import datetime
import pandas as pd
import re
from dotenv import load_dotenv
import difflib
from discord import SelectMenu, SelectOption, Interaction
from discord.ext import commands
from discord import Embed, Color
import sentences as st
import random
import asyncio


from functions import update_all_results, find_late_guys, calculation_of_the_number_of_match, get_player_matches

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)

load_dotenv()

token = os.getenv("token")

intents = discord.Intents.default() # Creating default intents
intents.members = True
intents.message_content = True # Giving our bot permission to send and read messages

bot = commands.Bot(command_prefix="/",intents=intents) # Creating bot

bot.remove_command('help')

ligueList = ["Coruscant","Tatooine","Alderaan","Kessel"]
pouleList = ["A","B","C","D"]

#107643272125513728
adminUsers = [408722513711988747,190863577391955969,107643272125513728]
chanelResultat = [1004513653015449620, 1158499018960277675]
chanelBot = [1158499018960277675,1161959267948044309]
channelAnnonce = 1004513446932512828

def find_closest_match(input_str, choices):
    matches = difflib.get_close_matches(input_str, choices, n=1,cutoff=0.3)  # n=1 signifie que nous voulons seulement la meilleure correspondance
    if matches:
        return matches[0]
    else:
        return None
    
def find_closest_match_0_8(input_str, choices):
    matches = difflib.get_close_matches(input_str, choices, n=1,cutoff=0.9)  # n=1 signifie que nous voulons seulement la meilleure correspondance
    if matches:
        return matches[0]
    else:
        return None

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    await bot.tree.sync()
    
    
@bot.event
async def on_command_error(ctx, error):
    
    
    if ctx.channel.id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await ctx.send(lostCanal, ephemeral=True)
        await asyncio.sleep(3)
        return
    
    
    lost_msg = random.choice(st.sentenceLost)
    await ctx.send(lost_msg,ephemeral=True)
    await asyncio.sleep(3)
    
    if isinstance(error, commands.CommandNotFound): 
        await help(ctx)
        
        
@bot.command()
async def help(ctx):
    
    if ctx.channel.id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await ctx.send(lostCanal, ephemeral=True)
        await asyncio.sleep(3)
        return
    
    embed = Embed(title="Besoin d'aide ?")
    embed.add_field(name="\u2001", value="\n", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)


    embed.add_field(name="**🏆\u2001\u2001/classement [nom de la ligue] [tableau entier]**", value="Permet d'afficher le classement de la Ligue", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)

    embed.add_field(name="**🏆\u2001\u2001/classement [nom de la ligue] [nom de la poule] [tableau entier]**", value="Permet d'afficher le classement de la Ligue pour la poule voulu", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)

    embed.add_field(name="**📜\u2001\u2001/liste [@joueur]**", value="Permet d'afficher le lien de la liste du joueur", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)

    embed.add_field(name="**📋\u2001\u2001/match [@joueur]**", value="permet d'afficher les matchs d'un joueur", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    embed.add_field(name="**☎️\u2001\u2001/retardataires **", value="(ADMIN ONLY) Permet de ping les joueurs avec le moins de match", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    embed.add_field(name="**🛰️\u2001\u2001/statusmatch **", value="Permet de voir l'évolution du nombre de match par poule et ligue", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)

    embed.add_field(name="**📊\u2001\u2001/graphwr**", value="Affiche les graphiques des win rate Joueur Bleu / Joueur rouge", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)


    embed.add_field(name="**📊\u2001\u2001/graphobjective**", value="Affiche les graphiques de la répartition des objectifs", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    embed.add_field(name="**📊\u2001\u2001/graphdeploiement**", value="Affiche les graphiques de la répartition des déploiments", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    embed.add_field(name="**📊\u2001\u2001/graphcondition**", value="Affiche les graphiques de la répartition des conditions", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    embed.add_field(name="**📊\u2001\u2001/graphkp**", value="Affiche les graphiques de la répartition des kill point", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    embed.add_field(name="**📊\u2001\u2001/graphvp**", value="Affiche les graphiques de la répartition des victory point", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    embed.add_field(name="**📊\u2001\u2001/graphrepartition**", value="Affiche les graphiques de la répartition des factions et des formats", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
     
    embed.add_field(name="**🔄\u2001\u2001/calcul**", value="(ADMIN ONLY) Force to calculate the results", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    await ctx.send(embed=embed)
  

@bot.tree.command(name="liste", description="afficher la liste d'un joueur")
async def slash_command(interaction: discord.Interaction, user: discord.User):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        return
    
    spyMessage = random.choice(st.sentenceSpy)
    await interaction.response.send_message(spyMessage, ephemeral=False)  # Envoi du message d'espionnage comme réponse initiale et éphémère
    await asyncio.sleep(3)

    # Chargez le CSV dans un DataFrame
    df = pd.read_csv("bdd/users.csv")
    
    user = f"{user.name}"
    user = find_closest_match(user, df["Pseudo Discord"].tolist())

    # Trouvez la ligne qui correspond au Pseudo Discord
    matching_row = df[df["Pseudo Discord"] == user]

    # S'il y a une correspondance, retournez le lien. Sinon, retournez une chaîne vide ou un message d'erreur
    if not matching_row.empty:
        await interaction.followup.send(content=f"Joueur trouvé : {user}\n{matching_row['Lien Armée'].iloc[0]}", ephemeral=False)
    else:
        await interaction.followup.send(content="Pas de lien trouvé pour cet utilisateur.", ephemeral=False)

    
@bot.tree.command(name="calcul", description="calcul csv")
async def slash_command(interaction: discord.Interaction):

    
    # Vérifiez si l'utilisateur est autorisé
    if interaction.user.id not in adminUsers:
        messageAdmin = random.choice(st.sentenceAdmin)
        await interaction.response.send_message(messageAdmin, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    await interaction.response.defer()
 
    answer = update_all_results()
    
    if answer == True:
        await interaction.followup.send(content="✅ Calcul fini!")
    else :            
        await interaction.followup.send(content="❌ Erreur Update")

    
    




@bot.event
async def on_message(message):
    
    
    if message.channel.id in chanelResultat : 
        lines = message.content.split("\n")
        
        if len(lines) == 10:
            
            missionList = ["Sabotage des Vaporisateurs Hydroponiques","Positions-Clés","Interception des Transmissions","Récupération de Ravitaillements","Echange d'Otages","Plasticage","Charges Explosives","Percée"]        
            deploiementList = ["Offensive Majeure","Positions Avancées","Véhicules Eclaireurs","La Longue Marche","Acculés","Lignes de Bataille","Confusion","Danger Proche"]
            conditionsList = ["Conditions Favorables","Largage de Ravitaillement","Environnement Hostile","Positions Fortifiées","Champs de Mines","Visibilité Limitée","Epuisés par la Guerre"]
            
            actualTime = datetime.now()
            mail = "martinpourrat@hotmail.com"
            try : 
                phase = lines[0].strip()
            except : 
                await message.channel.send("❌ Erreur : phase mal enregistrée ")
                return
            """
            try : 
                leagueName = lines[1].strip()
            except : 
                await message.channel.send("❌ Erreur : nom de league mal enregistré ")
                return
            
            try : 
                poule = lines[2].strip()
            except : 
                await message.channel.send("❌ Erreur : poule mal enregistrée ")
                return
            """
            try : 
                mission = lines[5].strip()
                mission = find_closest_match(mission,missionList)
                
            except : 
                await message.channel.send("❌ Erreur : mission mal enregistrée ")
                return
            
            try : 
                deploiement = lines[6].strip()
                deploiement = find_closest_match(deploiement,deploiementList)
            except : 
                await message.channel.send("❌ Erreur : deploiement mal enregistré ")
                return
            
            try : 
                conditions = lines[7].strip()
                conditions = find_closest_match(conditions,conditionsList)
            except : 
                await message.channel.send("❌ Erreur : condition mal enregistré ")
                return
            
            try : 
                kpBleu = int(lines[8].strip())
            except : 
                await message.channel.send("❌ Erreur : kp bleu  mal enregistré ")
                return
            
            try :    
                kpRouge = int(lines[9].strip())
            except : 
                await message.channel.send("❌ Erreur : kp rouge mal enregistré ")
                return
            try : 
                # Découper la chaîne de score
                score_parts = lines[4].split("-")
                score_1 = int(score_parts[0].strip())
                score_2 = int(score_parts[1].strip())
            except : 
                await message.channel.send("❌ Erreur : score mal enregistré ")
                return
            
            df = pd.read_csv("bdd/users.csv")
            
            try : 
                match = re.match(r'<@!?(\d+)>', lines[1])
            
                
                if match:
                    member_id = int(match.group(1))
                    member = await message.guild.fetch_member(member_id)
            
                    if member:
                        #joueurBleu = f"{member.name}#{member.discriminator}"  # Format : "username#discriminator"
                        joueurBleu = str(member.name)
                    else:
                        joueurBleu = "None"
                        
                else: 
                    await message.channel.send("❌ Erreur : Joueur Bleu mal enregistré ")
                    return

            except : 
                await message.channel.send("❌ Erreur : Joueur Bleu mal enregistré ")  
                return
              
            try :       
                match = re.match(r'<@!?(\d+)>', lines[2])

                if match:
                    member_id = int(match.group(1))
                    member = await message.guild.fetch_member(member_id)
                    
                    if member:
                        joueurRouge = str(member.name)
                        #joueurRouge = f"{member.name}#{member.discriminator}"
                    else:
                        joueurRouge = "None"
           
                else : 
                    await message.channel.send("❌ Erreur : Joueur Rouge mal enregistré ")
                    return
                
            except : 
                await message.channel.send("❌ Erreur : Joueur Rouge mal enregistré ")
                return
            
            try : 
                match = re.match(r'<@!?(\d+)>', lines[3])

                if match:
                    member_id = int(match.group(1))
                    member = await message.guild.fetch_member(member_id)
                    
                    if member:
                        winner = str(member.name)
                        #winner = f"{member.name}#{member.discriminator}"
                    else:
                        winner = "None"
                else : 
                    await message.channel.send("❌ Erreur : winner mal enregistré ")
                    return

            except : 
                await message.channel.send("❌ Erreur : le nom du winner mal enregistré ") 
                return

            # Assurez-vous que le score le plus élevé va au gagnant
            if winner == joueurBleu:
                scoreBleu = max(score_1, score_2)
                scoreRouge = min(score_1, score_2)
                winnerName = "Joueur Bleu"
            else:
                scoreBleu = min(score_1, score_2)
                scoreRouge = max(score_1, score_2)
                winnerName = "Joueur Rouge"
              
           
            try : 
                df = pd.read_csv('bdd/match.csv')
            except : 
                await message.channel.send("❌ Erreur : csv mal lu") 
                return
                
            # 2. Créer une nouvelle ligne sous forme de dictionnaire
            nouvelle_ligne = {
                "Horodateur": actualTime,
                "Adresse e-mail": mail,
                "Phase": phase,
                "Joueur Bleu": joueurBleu,
                "Joueur Rouge": joueurRouge,
                "Vainqueur": winnerName,
                "Points de Victoire Joueur Bleu (chiffre seulement)": scoreBleu,
                "Points de Victoire Joueur Rouge (chiffre seulement)": scoreRouge,
                "Kill Point Joueur Bleu (chiffre seulement)": kpBleu,
                "Kill Point Joueur Rouge (chiffre seulement)": kpRouge,
                "Objectif": mission,
                "Déploiement": deploiement,
                "Condition": conditions
            }

          
         
            # Colonnes à vérifier
            cols_to_check = [
                "Joueur Bleu", 
                "Joueur Rouge", 
                "Vainqueur", 
                "Points de Victoire Joueur Bleu (chiffre seulement)", 
                "Points de Victoire Joueur Rouge (chiffre seulement)"
            ]

                          
                # Convertir nouvelle_ligne en Series
            new_series = pd.Series(nouvelle_ligne, index=df.columns)
            try : 
            
    
                # Vérifier si la ligne existe déjà
                exists = (df[cols_to_check] == new_series[cols_to_check]).all(axis=1).any()

                # Si elle n'existe pas, ajouter la ligne
                if not exists:
                    df.loc[len(df)] = nouvelle_ligne
                else : 
                    await message.channel.send("❌ Erreur : duplication de ligne") 
                    return

                
            except : 
                await message.channel.send("❌ Erreur : csv , nouvelle ligne mal enregistrée") 
                return

            try :
                df.to_csv('bdd/match.csv', index=False)
            except : 
                await message.channel.send("❌ Erreur : sauvegarde csv ") 
                return
            
            await message.channel.send("✅ Match bien enregistré ")
            
            await message.channel.send("Update du classement et des graphs...")

            answer = update_all_results()
            
            if answer == True:
                await message.channel.send("✅ Update finie !")
            else :            
                await message.channel.send("❌ Erreur Update ")



    await bot.process_commands(message)




@bot.tree.command(name="statusmatch",description="retourne le statut des matchs")
async def slash_command(interaction: discord.Interaction):
    

    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:      
        return


    matchs = calculation_of_the_number_of_match()

   # Création d'un embed pour afficher les informations
    embed = discord.Embed(title="Progression du nombre de Matchs", color=0x03f8fc)  # Couleur bleu clair pour l'embed, modifiez à votre goût

    # En-tête du tableau
    header = "`Ligue      | Poule  | status`\n"
    header += "-"*35 + "\n"  # Une ligne de séparation

    # Construction des lignes du tableau
    table_rows = []
    for info in matchs:
        # Pour assurer un alignement correct, nous utiliserons la méthode ljust pour donner un espace fixe à chaque colonne
        ligue = info['Ligue'].ljust(10)
        poule = info['Poule'].ljust(6)
        
        # Calculer la progression en matches joués/non joués
        nb_played = int(info['nbMatchPlayed'])

        nb_not_played = 6 - nb_played
        progression = "▓" * nb_played + "░" * nb_not_played 

        row = f"`{ligue} | {poule} | {progression}`"
        table_rows.append(row)

    # Assemblage de l'en-tête et des lignes pour former le tableau complet
    table = header + '\n'.join(table_rows)
    embed.description = table

    await interaction.response.send_message(embed=embed)
    



@bot.tree.command(name="graphwr",description="get the wr diagram")
async def slash_command(interaction: discord.Interaction):
    
    messages_to_delete = []  # Liste pour stocker les messages à supprimer

    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    filesListe = ["Total", "Coruscant", "Tatooine", "Alderaan", "Kessel"]

    # Répondre initialement à l'interaction
    await interaction.response.send_message("Uploading graphs...", ephemeral=True)

    for file in filesListe:
        # Construire le chemin du fichier à partir de la liste
        file_path = f'Results/{file}/WrBlueRed.png'

        # Télécharger l'image sur Discord
        with open(file_path, 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        # Créer un embed pour l'image
        embed = discord.Embed(title=f"Win rate for {file}")

        # Utiliser l'URL de l'image téléchargée pour l'embed
        embed.set_image(url=image_url)
        
        embed.description = f'WR Blue/red for {file}'

        
        # Supprimer le message avec l'image téléchargée pour ne pas encombrer le canal
        await uploaded_image.delete()

        message = await interaction.channel.send(embed=embed)
                                                 
        # Ajouter le message à la liste des messages à supprimer
        messages_to_delete.append(message)

    # Attendre 60 secondes
    await asyncio.sleep(300)

    # Supprimer tous les messages
    for message in messages_to_delete:
        await message.delete()
            

@bot.tree.command(name="graphobjective",description="Get the list of objective")
async def slash_command(interaction: discord.Interaction):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    filesListe = ["Total", "Coruscant", "Tatooine", "Alderaan", "Kessel"]

    messages_to_delete = []
    # Répondre initialement à l'interaction
    await interaction.response.send_message("Uploading graphs...", ephemeral=True)

    for file in filesListe:
        # Construire le chemin du fichier à partir de la liste
        file_path = f'Results/{file}/PrObjectives.png'

        # Télécharger l'image sur Discord
        with open(file_path, 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        # Créer un embed pour l'image
        embed = discord.Embed(title=f"Objective rate for {file}")

        # Utiliser l'URL de l'image téléchargée pour l'embed
        embed.set_image(url=image_url)
        
        embed.description = f'Objective Blue/red for {file}'

        # Supprimer le message avec l'image téléchargée pour ne pas encombrer le canal
        await uploaded_image.delete()

        message = await interaction.channel.send(embed=embed)
                                                 
        # Ajouter le message à la liste des messages à supprimer
        messages_to_delete.append(message)

    # Attendre 60 secondes
    await asyncio.sleep(300)

    # Supprimer tous les messages
    for message in messages_to_delete:
        await message.delete()
        

@bot.tree.command(name="graphkp",description="Get the histogram of KP")
async def slash_command(interaction: discord.Interaction):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    filesListe = ["Total", "Coruscant", "Tatooine", "Alderaan", "Kessel"]

    messages_to_delete = []
    # Répondre initialement à l'interaction
    await interaction.response.send_message("Uploading graphs...", ephemeral=True)

    for file in filesListe:
        # Construire le chemin du fichier à partir de la liste
        file_path = f'Results/{file}/HistogramKP.png'

        # Télécharger l'image sur Discord
        with open(file_path, 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        # Créer un embed pour l'image
        embed = discord.Embed(title=f"Histogram KP for {file}")

        # Utiliser l'URL de l'image téléchargée pour l'embed
        embed.set_image(url=image_url)
        
        embed.description = f'Histogram KP  for {file}'

        # Supprimer le message avec l'image téléchargée pour ne pas encombrer le canal
        await uploaded_image.delete()

        message = await interaction.channel.send(embed=embed)
                                                 
        # Ajouter le message à la liste des messages à supprimer
        messages_to_delete.append(message)

    # Attendre 60 secondes
    await asyncio.sleep(300)

    # Supprimer tous les messages
    for message in messages_to_delete:
        await message.delete()




@bot.tree.command(name="graphvp",description="Get the histogram of VP")
async def slash_command(interaction: discord.Interaction):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    filesListe = ["Total", "Coruscant", "Tatooine", "Alderaan", "Kessel"]

    messages_to_delete = []
    # Répondre initialement à l'interaction
    await interaction.response.send_message("Uploading graphs...", ephemeral=True)

    for file in filesListe:
        # Construire le chemin du fichier à partir de la liste
        file_path = f'Results/{file}/HistogramKV.png'

        # Télécharger l'image sur Discord
        with open(file_path, 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        # Créer un embed pour l'image
        embed = discord.Embed(title=f"Histogram VP for {file}")

        # Utiliser l'URL de l'image téléchargée pour l'embed
        embed.set_image(url=image_url)
        
        embed.description = f'Histogram VP for {file}'

        # Supprimer le message avec l'image téléchargée pour ne pas encombrer le canal
        await uploaded_image.delete()

        message = await interaction.channel.send(embed=embed)
                                                 
        # Ajouter le message à la liste des messages à supprimer
        messages_to_delete.append(message)

    # Attendre 60 secondes
    await asyncio.sleep(300)

    # Supprimer tous les messages
    for message in messages_to_delete:
        await message.delete()
        

@bot.tree.command(name="graphrepartition",description="Get the reparition of format and faction")
async def slash_command(interaction: discord.Interaction):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    filesListe = ["Total", "Coruscant", "Tatooine", "Alderaan", "Kessel"]

    messages_to_delete = []
    # Répondre initialement à l'interaction
    await interaction.response.send_message("Uploading graphs...", ephemeral=True)

    for file in filesListe:
        # Construire le chemin du fichier à partir de la liste
        file_path = f'Results/{file}/FactionFormat.png'

        # Télécharger l'image sur Discord
        with open(file_path, 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        # Créer un embed pour l'image
        embed = discord.Embed(title=f"Repartition Faction/Format for {file}")

        # Utiliser l'URL de l'image téléchargée pour l'embed
        embed.set_image(url=image_url)
        
        embed.description = f'Histogram Faction/Format  for {file}'

        # Supprimer le message avec l'image téléchargée pour ne pas encombrer le canal
        await uploaded_image.delete()

        message = await interaction.channel.send(embed=embed)
                                                 
        # Ajouter le message à la liste des messages à supprimer
        messages_to_delete.append(message)

    # Attendre 60 secondes
    await asyncio.sleep(300)

    # Supprimer tous les messages
    for message in messages_to_delete:
        await message.delete()

@bot.tree.command(name="graphdeploiement",description="Get the list of deploiement")
async def slash_command(interaction: discord.Interaction):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    filesListe = ["Total", "Coruscant", "Tatooine", "Alderaan", "Kessel"]
    messages_to_delete = []
    # Répondre initialement à l'interaction
    await interaction.response.send_message("Uploading graphs...", ephemeral=True)

    for file in filesListe:
        # Construire le chemin du fichier à partir de la liste
        file_path = f'Results/{file}/PrDeploiement.png'

        # Télécharger l'image sur Discord
        with open(file_path, 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        # Créer un embed pour l'image
        embed = discord.Embed(title=f"Deploiement rate for {file}")

        # Utiliser l'URL de l'image téléchargée pour l'embed
        embed.set_image(url=image_url)
        
        embed.description = f'Deploiement Blue/red for {file}'

        # Supprimer le message avec l'image téléchargée pour ne pas encombrer le canal
        await uploaded_image.delete()

        message = await interaction.channel.send(embed=embed)
                                                 
        # Ajouter le message à la liste des messages à supprimer
        messages_to_delete.append(message)

    # Attendre 60 secondes
    await asyncio.sleep(300)

    # Supprimer tous les messages
    for message in messages_to_delete:
        await message.delete()


@bot.tree.command(name="graphcondition",description="Get the list of condition")
async def slash_command(interaction: discord.Interaction):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    filesListe = ["Total", "Coruscant", "Tatooine", "Alderaan", "Kessel"]
    messages_to_delete = []
    # Répondre initialement à l'interaction
    await interaction.response.send_message("Uploading graphs...", ephemeral=True)

    for file in filesListe:
        # Construire le chemin du fichier à partir de la liste
        file_path = f'Results/{file}/PrCondition.png'

        # Télécharger l'image sur Discord
        with open(file_path, 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        # Créer un embed pour l'image
        embed = discord.Embed(title=f"Condition rate for {file}")

        # Utiliser l'URL de l'image téléchargée pour l'embed
        embed.set_image(url=image_url)
        
        embed.description = f'Condition Blue/red for {file}'

        # Supprimer le message avec l'image téléchargée pour ne pas encombrer le canal
        await uploaded_image.delete()

        message = await interaction.channel.send(embed=embed)
                                                 
        # Ajouter le message à la liste des messages à supprimer
        messages_to_delete.append(message)

    # Attendre 60 secondes
    await asyncio.sleep(300)

    # Supprimer tous les messages
    for message in messages_to_delete:
        await message.delete()





@bot.tree.command(name="match",description="Get the match of a player")
async def slash_command(interaction: discord.Interaction, player_name: discord.User):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return

    
    # Chargez le CSV dans un DataFrame
    df = pd.read_csv("bdd/users.csv")
    
    player_name = f"{player_name.name}"
    player_name = find_closest_match(player_name, df["Pseudo Discord"].tolist())
    matches = get_player_matches(player_name)
        
    # Assurez-vous que votre bot est connecté et que vous avez un objet channel pour envoyer des messages
    embed = discord.Embed(title=f"Matchs de {player_name}", description="\n")

    for match in matches:
        # Déterminer la pastille en fonction de 'awin'
        pastille = '🟢' if match['awin'] else '🔴'
        
        match_info = (f"**Phase:** {match['Phase']}\n"
                    f"**Bleu:** {match['Joueur Bleu']}\n"
                    f"**Rouge:** {match['Joueur Rouge']}\n"
                    f"**Vainqueur:** {match['Vainqueur']}\n"
                    f"**Objectif:** {match['Objectif']}\n"
                    f"**Déploiement:** {match['Déploiement']}\n"
                    f"**Condition:** {match['Condition']}\n"
                    f"**PV Bleu:** {match['PV Bleu']}\n"
                    f"**PV Rouge:** {match['PV Rouge']}\n"
                    f"**KP Bleu:** {match['KP Bleu']}\n"
                    f"**KP Rouge:** {match['KP Rouge']}")
        embed.add_field(name=f"{pastille} Match du {match['Horodateur']}", value=match_info + "\n", inline=False)

    await interaction.response.send_message(embed=embed)



@bot.tree.command(name="bid",description="Get the list of bid")
async def slash_command(interaction: discord.Interaction):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    filesListe = ["Total", "Coruscant", "Tatooine", "Alderaan", "Kessel"]
    messages_to_delete = []
    # Répondre initialement à l'interaction
    await interaction.response.send_message("Uploading graphs...", ephemeral=True)

    for file in filesListe:
        # Construire le chemin du fichier à partir de la liste
        file_path = f'Results/{file}/meanBid.png'

        # Télécharger l'image sur Discord
        with open(file_path, 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        # Créer un embed pour l'image
        embed = discord.Embed(title=f"bid rate for {file}")

        # Utiliser l'URL de l'image téléchargée pour l'embed
        embed.set_image(url=image_url)
        
        embed.description = f'bid Blue/red for {file}'

        # Supprimer le message avec l'image téléchargée pour ne pas encombrer le canal
        await uploaded_image.delete()

        message = await interaction.channel.send(embed=embed)
                                                 
        # Ajouter le message à la liste des messages à supprimer
        messages_to_delete.append(message)

    # Attendre 60 secondes
    await asyncio.sleep(300)

    # Supprimer tous les messages
    for message in messages_to_delete:
        await message.delete()



def split_message(content):
    """Divise le contenu en plusieurs morceaux de moins de 2000 caractères chacun."""
    return [content[i:i+2000] for i in range(0, len(content), 2000)]


@bot.tree.command(name="retardataires",description="PING LES NULS")
async def slash_command(interaction: discord.Interaction):
     
        # Obtenez le canal
    channel = interaction.guild.get_channel(channelAnnonce)
    
    print(channel)
    
    # Vérifiez si l'utilisateur est autorisé
    if interaction.user.id not in adminUsers:
        messageAdmin = random.choice(st.sentenceAdmin)
        await interaction.response.send_message(messageAdmin, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
 
    # Récupérer tous les noms des membres du serveur
    member_names = [member.name for member in interaction.guild.members]
    membersToPing = find_late_guys()

    pinged_members = []
    not_found_members = []

    guild = interaction.guild
    memberName = [member.name for member in guild.members]

    for memberId in membersToPing:
        

        if str(memberId) in memberName: 
            id = discord.utils.get(guild.members,name =str(memberId))
            messageRetard = random.choice(st.sentenceLate).replace("[Joueur]", f"{id.mention}")
            pinged_members.append(messageRetard)

        else:
            not_found_members.append(str(memberId))

    pinged_messages = " ".join(pinged_members)
    split_pinged_messages = split_message(pinged_messages)

    for message_part in split_pinged_messages:
        await channel.send(message_part)


    if not_found_members:
        await channel.send("Les utilisateurs suivants n'ont pas été trouvés: " + ", ".join(not_found_members))
        
    await interaction.response.send_message("✅ Message envoyé !")



@bot.tree.command(name="classement", description="afficher le classement")
async def slash_command(interaction: discord.Interaction,ligue: str, poule_name:str = None, full : bool = False):
    
    # Vérifiez si la commande est exécutée dans le canal autorisé
    if interaction.channel_id not in chanelBot:
        lostCanal = random.choice(st.sentenceLostCanal)
        await interaction.response.send_message(lostCanal, ephemeral=True)
        await asyncio.sleep(3)        
        return
    
    lienClassement = "bdd/classement.csv"
   
    dfClassement = pd.read_csv(lienClassement,delimiter = ",")
    
    ligue = find_closest_match(ligue , ligueList)

    dfClassement = dfClassement[dfClassement["Ligue"] == ligue]
    if poule_name : 
        pouleList = ["A","B","C","D"]
        poule_name = find_closest_match(poule_name , pouleList)
        pouleList = [poule_name]
    else : 
        pouleList = sorted(dfClassement["Poule"].unique())
    
 
    
    if dfClassement.empty:
        await interaction.channel.send("❌ Erreur : ligue ou poule mal enregistrée ")
        return
    
    
    if full == False : 
        
        dfClassement = dfClassement[["Pseudo","Poule","victory" ,"defeat","points"]]
        dfClassement = dfClassement.rename(columns={"victory": "V"})
        dfClassement = dfClassement.rename(columns={"defeat": "D"})
        dfClassement = dfClassement.rename(columns={"points": "PTS"})


        #Raccourcir chaque valeur du DataFrame à 8 caractères max
        for col in dfClassement.columns:

            if col == "V":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:2].rjust(2))
            elif col == "D":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:2].rjust(2))
            elif col == "PTS":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:3].rjust(3))
            elif col == "   Poule":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:5].rjust(5))
            else :  
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:8].rjust(8))
            
        dfClassement.columns = [
            col[:2].rjust(2) if col == "V" or col == "D" 
            else col[:3].rjust(3) if col == "PTS" 
            else col[:5].rjust(5) if col == "Poule" 
            else col[:8].rjust(8) 
            for col in dfClassement.columns
        ]
        total_content = ""
    

        
        for poule in pouleList:

            df_poule = dfClassement[dfClassement['Poule'].str.strip() == poule]
            df_poule = df_poule[["  Pseudo"," V" ," D","PTS"]]


            # Convertir ce DataFrame comme vous l'avez fait précédemment
            header = ' | '.join(df_poule.columns)
            separator = '-|-'.join(['-' * len(col) for col in df_poule.columns])
            rows_as_strings = df_poule.apply(lambda row: ' | '.join(row), axis=1)
            # Titre pour la poule actuelle
            poule_title = f"### Poule {poule} ###\n"

            content = f"```\n| {header} |\n| {separator} |\n" + '\n'.join('| ' + row + ' |' for row in rows_as_strings) + "\n```"

            # Concatène le titre de la poule et son contenu au contenu total
            total_content += poule_title + content + "\n"  # Deux sauts de ligne pour un espacement

            
        # Si le contenu total est trop long pour un message Discord, vous devez le tronquer.
        if len(total_content) > 2000:
            total_content = total_content[:2000] + "..."

        with open(f'media/baniere/{ligue}.png', 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        embed = discord.Embed(title=f"Classement {ligue}")
        embed.set_image(url=image_url)
        embed.description = total_content

        await uploaded_image.delete()
        await interaction.response.send_message(embed=embed)
        return
    
    else : 
            
        dfClassement = dfClassement[["Pseudo","Poule","victory" ,"defeat","points","SoS","sumKP","sumPV"]]
        dfClassement = dfClassement.rename(columns={"victory": "V"})
        dfClassement = dfClassement.rename(columns={"defeat": "D"})
        dfClassement = dfClassement.rename(columns={"points": "PTS"})



        #Raccourcir chaque valeur du DataFrame à 8 caractères max
        for col in dfClassement.columns:

            if col == "V":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:2].rjust(2))
            elif col == "D":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:2].rjust(2))
            elif col == "PTS":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:3].rjust(3))
            elif col == "   Poule":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:5].rjust(5))
            elif col == "sumPV":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:5].rjust(5))
            elif col == "SoS":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:3].rjust(3))
            elif col == "sumKP":
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:5].rjust(5))
            else :  
                dfClassement[col] = dfClassement[col].astype(str).apply(lambda x: x[:8].rjust(8))
            
        dfClassement.columns = [
            col[:2].rjust(2) if col == "V" or col == "D" 
            else col[:3].rjust(3) if col == "PTS" 
            else col[:5].rjust(5) if col == "Poule" 
            else col[:5].rjust(5) if col == "sumPV" 
            else col[:3].rjust(3) if col == "SoS" 
            else col[:5].rjust(5) if col == "sumKP" 
            else col[:8].rjust(8) 
            for col in dfClassement.columns
        ]
        total_content = ""
    

        
        for poule in pouleList:

            df_poule = dfClassement[dfClassement['Poule'].str.strip() == poule]
            df_poule = df_poule[["  Pseudo"," V" ," D","PTS","SoS","sumKP","sumPV"]]


            # Convertir ce DataFrame comme vous l'avez fait précédemment
            header = ' | '.join(df_poule.columns)
            separator = '-|-'.join(['-' * len(col) for col in df_poule.columns])
            rows_as_strings = df_poule.apply(lambda row: ' | '.join(row), axis=1)
            # Titre pour la poule actuelle
            poule_title = f"### Poule {poule} ###\n"

            content = f"```\n| {header} |\n| {separator} |\n" + '\n'.join('| ' + row + ' |' for row in rows_as_strings) + "\n```"

            # Concatène le titre de la poule et son contenu au contenu total
            total_content += poule_title + content + "\n"  # Deux sauts de ligne pour un espacement

            
        # Si le contenu total est trop long pour un message Discord, vous devez le tronquer.
        if len(total_content) > 2000:
            total_content = total_content[:2000] + "..."

        with open(f'media/baniere/{ligue}.png', 'rb') as f:
            uploaded_image = await interaction.channel.send(file=discord.File(f))
            image_url = uploaded_image.attachments[0].url

        embed = discord.Embed(title=f"Classement {ligue}")
        embed.set_image(url=image_url)
        embed.description = total_content

        await uploaded_image.delete()
        await interaction.response.send_message(embed=embed)
        return

    


bot.run(token)