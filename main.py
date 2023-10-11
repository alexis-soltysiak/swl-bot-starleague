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
from discord.ext import commands, menus
from discord import Embed, Color
import sentences as st
import random
import asyncio


from functions import update_all_results, find_late_guys

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
adminUsers = [408722513711988747,190863577391955969]
chanelResultat = [1004513653015449620, 1158499018960277675]
chanelBot = [1158499018960277675,1004637828342362133]


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
    await ctx.send(lost_msg)
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


    embed.add_field(name="**🏆\u2001\u2001/classement [nom de la ligue]**", value="Permet d'afficher le classement de la Ligue", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)

    embed.add_field(name="**🏆\u2001\u2001/classement [nom de la ligue] [nom de la poule] **", value="Permet d'afficher le classement de la Ligue pour la poule voulu", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)

    embed.add_field(name="**📜\u2001\u2001/liste [@joueur]**", value="Permet d'afficher le lien de la liste du joueur", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)

    embed.add_field(name="**☎️\u2001\u2001/retardataires **", value="(ADMIN ONLY) Permet de ping les joueurs avec le moins de match", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)

    embed.add_field(name="**📊\u2001\u2001/wr**", value="Affiche les graphiques des win rate Joueur Bleu / Joueur rouge", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)


    embed.add_field(name="**📊\u2001\u2001/objective**", value="Affiche les graphiques de la répartition des objectifs", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    
    embed.add_field(name="**📊\u2001\u2001/deploiement**", value="Affiche les graphiques de la répartition des déploiments", inline=False)
    embed.add_field(name="\u2001", value="\n", inline=False)
    
    embed.add_field(name="**📊\u2001\u2001/condition**", value="Affiche les graphiques de la répartition des conditions", inline=False)
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
        await asyncio.sleep(3)        
        return
    
    spyMessage = random.choice(st.sentenceSpy)
    await interaction.response.send_message(spyMessage, ephemeral=True)
    await asyncio.sleep(3)

    # Chargez le CSV dans un DataFrame
    df = pd.read_csv("bdd/users.csv")
    
        
    user = f"{user.name}"
    
    user = find_closest_match(user, df["Pseudo Discord"].tolist())


    # Trouvez la ligne qui correspond au Pseudo Discord
    matching_row = df[df["Pseudo Discord"] == user]

    # S'il y a une correspondance, retournez le lien. Sinon, retournez une chaîne vide ou un message d'erreur
    if not matching_row.empty:
        await interaction.response.send_message(content=f"Joueur trouvé : {user}\n{matching_row['Lien Armée'].iloc[0]}")

    else:
        await interaction.response.send_message(content="Pas de lien trouvé pour cet utilisateur.")

    
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
        
        if len(lines) == 12:
            
            actualTime = datetime.now()
            mail = "martinpourrat@hotmail.com"
            try : 
                phase = lines[0].strip()
            except : 
                await message.channel.send("❌ Erreur : phase mal enregistrée ")
                return

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
            
            try : 
                mission = lines[7].strip()
            except : 
                await message.channel.send("❌ Erreur : mission mal enregistrée ")
                return
            
            try : 
                deploiement = lines[8].strip()
            except : 
                await message.channel.send("❌ Erreur : deploiement mal enregistré ")
                return
            
            try : 
                conditions = lines[9].strip()
            except : 
                await message.channel.send("❌ Erreur : condition mal enregistré ")
                return
            
            try : 
                kpBleu = int(lines[10].strip())
            except : 
                await message.channel.send("❌ Erreur : kp bleu  mal enregistré ")
                return
            
            try :    
                kpRouge = int(lines[11].strip())
            except : 
                await message.channel.send("❌ Erreur : kp rouge mal enregistré ")
                return
            try : 
                # Découper la chaîne de score
                score_parts = lines[6].split("-")
                score_1 = int(score_parts[0].strip())
                score_2 = int(score_parts[1].strip())
            except : 
                await message.channel.send("❌ Erreur : score mal enregistré ")
                return
            try : 
                match = re.match(r'<@!?(\d+)>', lines[3])
                
                if match:
                    member_id = int(match.group(1))
                    member = await message.guild.fetch_member(member_id)
                    
            
                    if member:
                        joueurBleu = f"{member.name}#{member.discriminator}"  # Format : "username#discriminator"
                    else:
                        joueurBleu = "None"
                else: 
                    await message.channel.send("❌ Erreur : Joueur Bleu mal enregistré ")
                    return

            except : 
                await message.channel.send("❌ Erreur : Joueur Bleu mal enregistré ")  
                return
              
            try :       
                match = re.match(r'<@!?(\d+)>', lines[4])

                if match:
                    member_id = int(match.group(1))
                    member = await message.guild.fetch_member(member_id)
                    
                    if member:
                        joueurRouge = f"{member.name}#{member.discriminator}"
                    else:
                        joueurRouge = "None"
           
                else : 
                    await message.channel.send("❌ Erreur : Joueur Rouge mal enregistré ")
                    return
                
            except : 
                await message.channel.send("❌ Erreur : Joueur Rouge mal enregistré ")
                return
            
            try : 
                match = re.match(r'<@!?(\d+)>', lines[5])

                if match:
                    member_id = int(match.group(1))
                    member = await message.guild.fetch_member(member_id)
                    
                    if member:
                        winner = f"{member.name}#{member.discriminator}"
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
            else:
                scoreBleu = min(score_1, score_2)
                scoreRouge = max(score_1, score_2)
              
           
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
                "Vainqueur": winner,
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
            
            await message.channel.send("✅ Match bien enrigstré ")
            
            await message.channel.send("Update du classement et des graphs...")

            answer = update_all_results()
            
            if answer == True:
                await message.channel.send("✅ Update finie !")
            else :            
                await message.channel.send("❌ Erreur Update ")



    await bot.process_commands(message)



@bot.tree.command(name="wr",description="get the wr diagram")
async def slash_command(interaction: discord.Interaction):
    
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

        # Envoyer le message embed au canal
        message = await interaction.channel.send(embed=embed)  
        await asyncio.sleep(60)

        # Supprimer le message
        await message.delete()
        

@bot.tree.command(name="objective",description="Get the list of objective")
async def slash_command(interaction: discord.Interaction):
    
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

        # Envoyer le message embed au canal
        await interaction.channel.send(embed=embed)


@bot.tree.command(name="deploiement",description="Get the list of deploiement")
async def slash_command(interaction: discord.Interaction):
    
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

        # Envoyer le message embed au canal
        await interaction.channel.send(embed=embed)


@bot.tree.command(name="condition",description="Get the list of condition")
async def slash_command(interaction: discord.Interaction):
    
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

        # Envoyer le message embed au canal
        await interaction.channel.send(embed=embed)



@bot.tree.command(name="bid",description="Get the list of bid")
async def slash_command(interaction: discord.Interaction):
    
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

        # Envoyer le message embed au canal
        await interaction.channel.send(embed=embed)





@bot.tree.command(name="retardataires",description="PING LES NULS")
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
 
    # Récupérer tous les noms des membres du serveur
    member_names = [member.name for member in interaction.guild.members]
    membersToPing = find_late_guys()

    pinged_members = []
    not_found_members = []

    for memberToPing in membersToPing:
        closest_name = find_closest_match_0_8(memberToPing, member_names)
        user = discord.utils.find(lambda m: m.name.startswith(closest_name), interaction.guild.members)
        
        if user:
            pinged_members.append(f"{memberToPing} alias {user.mention} il semblerait que tu sois en retard <3 \n")
        else:
            not_found_members.append(memberToPing)

    if pinged_members:
        await interaction.response.send_message(" ".join(pinged_members))

    if not_found_members:
        await interaction.response.send_message("Les utilisateurs suivants n'ont pas été trouvés: " + ", ".join(not_found_members))




@bot.tree.command(name="classement", description="afficher le classement")
async def slash_command(interaction: discord.Interaction,ligue: str, poule_name:str = None):
    
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

    


bot.run(token)