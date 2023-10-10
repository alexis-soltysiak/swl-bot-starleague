# Importing Some stuff for our bot
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

from functions import update_all_results

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)

load_dotenv()

token = os.getenv("token")

intents = discord.Intents.default() # Creating default intents
intents.message_content = True # Giving our bot permission to send and read messages

bot = commands.Bot(command_prefix="/",intents=intents) # Creating bot

ligueList = ["Coruscant","Tatooine","Alderaan","Kessel"]
pouleList = ["A","B","C","D"]

def find_closest_match(input_str, choices):
    matches = difflib.get_close_matches(input_str, choices, n=1,cutoff=0.3)  # n=1 signifie que nous voulons seulement la meilleure correspondance
    if matches:
        return matches[0]
    else:
        return None
    
    
# Our First Command
@bot.command()
async def hello(ctx):
    await ctx.send("Hey!")

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    await bot.tree.sync()
    
    
@bot.tree.command(name="liste", description="afficher la liste d'un joueur")
async def slash_command(interaction: discord.Interaction, user: discord.User):

    # Chargez le CSV dans un DataFrame
    df = pd.read_csv("bdd/users.csv")
    
    
        
    user = f"{user.name}"
    
    print("user" ,user)
    user = find_closest_match(user, df["Pseudo Discord"].tolist())


    # Trouvez la ligne qui correspond au Pseudo Discord
    matching_row = df[df["Pseudo Discord"] == user]
    
    print(user)
    
    # S'il y a une correspondance, retournez le lien. Sinon, retournez une chaîne vide ou un message d'erreur
    if not matching_row.empty:
        await interaction.response.send_message(content=f"Joueur trouvé : {user}\n{matching_row['Lien Armée'].iloc[0]}")

    else:
        await interaction.response.send_message(content="Pas de lien trouvé pour cet utilisateur.")

    
@bot.tree.command(name="calcul", description="calcul csv")
async def slash_command(interaction: discord.Interaction):
    
    await interaction.response.defer()
    
    #waitingMessage = await interaction.channel.send("Chargement en cours...")

    # Exécutez la fonction qui prend du temps
    update_all_results()

    #await waitingMessage.delete()
    
    print("gogogo")
    await interaction.followup.send(content="✅ calcul fini!")




        
    

@bot.event
async def on_message(message):
    
    if message.channel.id == 1158499018960277675:  # Remplacez XXXXXXXXXXXXX par l'ID de votre canal
        lines = message.content.split("\n")
        
        if len(lines) >= 11:
            
            actualTime = datetime.now()
            mail = "martinpourrat@hotmail.com"
            try : 
                phase = lines[0].strip()
            except : 
                await message.channel.send("❌ Erreur : phase mal enregistrée ")

            try : 
                leagueName = lines[1].strip()
            except : 
                await message.channel.send("❌ Erreur : nom de league mal enregistré ")
                
            try : 
                poule = lines[2].strip()
            except : 
                await message.channel.send("❌ Erreur : poule mal enregistrée ")
                
            try : 
                mission = lines[7].strip()
            except : 
                await message.channel.send("❌ Erreur : mission mal enregistrée ")
                
            try : 
                deploiement = lines[8].strip()
            except : 
                await message.channel.send("❌ Erreur : deploiement mal enregistré ")
                
            try : 
                conditions = lines[9].strip()
            except : 
                await message.channel.send("❌ Erreur : condition mal enregistré ")
            
            try : 
                kpBleu = int(lines[10].strip())
            except : 
                await message.channel.send("❌ Erreur : kp bleu  mal enregistré ")
            
            try :    
                kpRouge = int(lines[11].strip())
            except : 
                await message.channel.send("❌ Erreur : kp rouge mal enregistré ")

            try : 
                # Découper la chaîne de score
                score_parts = lines[6].split("-")
                score_1 = int(score_parts[0].strip())
                score_2 = int(score_parts[1].strip())
            except : 
                await message.channel.send("❌ Erreur : score mal enregistré ")

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

            except : 
                await message.channel.send("❌ Erreur : Joueur Bleu mal enregistré ")  
              
            try :       
                match = re.match(r'<@!?(\d+)>', lines[4])

                if match:
                    member_id = int(match.group(1))
                    member = await message.guild.fetch_member(member_id)
                    
                    if member:
                        joueurRouge = f"{member.name}#{member.discriminator}"
                    else:
                        joueurRouge = "None"
                        
                    print("eeee")
                else : 
                    await message.channel.send("❌ Erreur : Joueur Rouge mal enregistré ")
            except : 
                await message.channel.send("❌ Erreur : Joueur Rouge mal enregistré ")
            
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

            except : 
                await message.channel.send("❌ Erreur : le nom du winner mal enregistré ") 

            # Assurez-vous que le score le plus élevé va au gagnant
            if winner == joueurBleu:
                scoreBleu = max(score_1, score_2)
                scoreRouge = min(score_1, score_2)
            else:
                scoreBleu = min(score_1, score_2)
                scoreRouge = max(score_1, score_2)
              
            """  
            print(f"league Name :  {leagueName}")
            print(f"Poule: {poule}")
            print(f"Joueur Bleu: {joueurBleu}")
            print(f"Joueur Rouge: {joueurRouge}")
            print(f"Winner: {winner}")
            print(f"Score Bleu: {scoreBleu}")
            print(f"Score Rouge: {scoreRouge}")
            print(f"Mission: {mission}")
            print(f"Deploiement: {deploiement}")
            print(f"Conditions: {conditions}")
            print(f"KP Bleu: {kpBleu}")
            print(f"KP Rouge: {kpRouge}")
            """ 
            
            try : 
                df = pd.read_csv('bdd/match.csv')
            except : 
                await message.channel.send("❌ Erreur : csv mal lu") 
                
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

            try : 
                df.loc[len(df)] = nouvelle_ligne
            except : 
                await message.channel.send("❌ Erreur : csv , nouvelle ligne mal enregistrée") 

            try :
                df.to_csv('bdd/match.csv', index=False)
            except : 
                await message.channel.send("❌ Erreur : sauvegarde csv ") 
            
            await message.channel.send("✅ Match bien enrigstré ")


    await bot.process_commands(message)



@bot.tree.command(name="wr",description="get the wr diagram")
async def slash_command(interaction: discord.Interaction):
    
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
        await interaction.channel.send(embed=embed)
        

@bot.tree.command(name="objective",description="Get the list of objective")
async def slash_command(interaction: discord.Interaction):
    
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


"""

@bot.tree.command(name="factionformat",description="Get the list of condition")
async def slash_command(interaction: discord.Interaction):
    
    filesListe = ["Total", "Coruscant", "Tatooine", "Alderaan", "Kessel"]

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
        embed = discord.Embed(title=f"FactionFormat rate for {file}")

        # Utiliser l'URL de l'image téléchargée pour l'embed
        embed.set_image(url=image_url)
        
        embed.description = f'FactionFormat Blue/red for {file}'

        # Supprimer le message avec l'image téléchargée pour ne pas encombrer le canal
        await uploaded_image.delete()

        # Envoyer le message embed au canal
        await interaction.channel.send(embed=embed)


"""


@bot.tree.command(name="bid",description="Get the list of bid")
async def slash_command(interaction: discord.Interaction):
    
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



@bot.tree.command(name="classement", description="afficher le classement")
async def slash_command(interaction: discord.Interaction,ligue: str, poule_name:str = None):
    
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

     

@bot.command()
async def av(ctx,member: discord.Member):
    await ctx.send(member.display_avatar)




bot.run(token)