import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from random import choice, randint

# Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Définir les intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

# Créer une instance du bot
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()  # Synchronise les commandes slash au démarrage

bot = MyBot()

# Événement déclenché quand le bot est prêt
@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

# ======================
# COMMANDES DE MODÉRATION
# ======================

# Commande pour kick un membre
@bot.tree.command(name="kick", description="Expulse un membre du serveur.")
@app_commands.describe(member="Membre à expulser", reason="Raison de l'expulsion")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.name} a été expulsé pour la raison : {reason}", ephemeral=True)

# Commande pour bannir un membre
@bot.tree.command(name="ban", description="Bannit un membre du serveur.")
@app_commands.describe(member="Membre à bannir", reason="Raison du bannissement")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member.name} a été banni pour la raison : {reason}", ephemeral=True)

# Commande pour débannir un membre
@bot.tree.command(name="unban", description="Débannit un membre du serveur.")
@app_commands.describe(member="Nom complet du membre à débannir (format : Nom#1234)")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, member: str):
    banned_users = await interaction.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"{user.name}#{user.discriminator} a été débanni.", ephemeral=True)
            return
    await interaction.response.send_message("Membre non trouvé.", ephemeral=True)

# Commande pour effacer des messages
@bot.tree.command(name="clear", description="Efface un certain nombre de messages dans un canal.")
@app_commands.describe(amount="Nombre de messages à effacer")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"{amount} messages ont été supprimés.", ephemeral=True)

# ======================
# COMMANDES DE DIVERTISSEMENT
# ======================

# Commande 8ball : répond à une question avec une réponse aléatoire
@bot.tree.command(name="eightball", description="Pose une question et le bot répond.")
@app_commands.describe(question="Votre question")
async def eightball(interaction: discord.Interaction, question: str):
    responses = [
        "C'est certain.",
        "Oui, absolument.",
        "Je pense que oui.",
        "Peut-être.",
        "Je ne sais pas.",
        "Probablement pas.",
        "Non.",
        "C'est impossible.",
    ]
    await interaction.response.send_message(f"🎱 Question : {question}\nRéponse : {choice(responses)}")

# Commande pour faire dire un message au bot
@bot.tree.command(name="say", description="Fait dire quelque chose au bot.")
@app_commands.describe(message="Message que le bot doit dire")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

# Commande pour lancer un dé
@bot.tree.command(name="roll", description="Lance un dé.")
@app_commands.describe(sides="Nombre de faces du dé (par défaut : 6)")
async def roll(interaction: discord.Interaction, sides: int = 6):
    result = randint(1, sides)
    await interaction.response.send_message(f"🎲 Résultat : {result}")

# ======================
# COMMANDES UTILITAIRES
# ======================

# Commande pour afficher les informations du serveur
@bot.tree.command(name="serverinfo", description="Affiche des informations sur le serveur.")
async def serverinfo(interaction: discord.Interaction):
    server = interaction.guild
    embed = discord.Embed(title="Informations du serveur", color=discord.Color.blue())
    embed.add_field(name="Nom", value=server.name, inline=False)
    embed.add_field(name="Membres", value=server.member_count, inline=False)
    embed.add_field(name="Créé le", value=server.created_at.strftime("%d/%m/%Y"), inline=False)
    await interaction.response.send_message(embed=embed)

# Commande pour afficher les informations de l'utilisateur
@bot.tree.command(name="userinfo", description="Affiche des informations sur un utilisateur.")
@app_commands.describe(member="Membre dont vous souhaitez voir les informations (par défaut : vous)")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user  # Utilise l'utilisateur si aucun membre spécifié
    embed = discord.Embed(title="Informations utilisateur", color=discord.Color.green())
    embed.add_field(name="Nom", value=member.name, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="A rejoint le", value=member.joined_at.strftime("%d/%m/%Y"), inline=False)
    embed.set_thumbnail(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

# Commande pour ping le bot et mesurer la latence
@bot.tree.command(name="ping", description="Affiche la latence du bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # Latence en ms
    await interaction.response.send_message(f"🏓 Pong ! Latence : {latency}ms")

# ======================
# COMMANDE DE STATUT
# ======================

# Commande pour changer le statut du bot
@bot.tree.command(name="setstatus", description="Change le statut du bot.")
@app_commands.describe(status="Statut à définir", activity="Activité à associer au statut")
async def setstatus(interaction: discord.Interaction, status: str, activity: str = None):
    status_mapping = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
        "invisible": discord.Status.invisible
    }

    activity_mapping = {
        "playing": discord.Game,
        "streaming": discord.Streaming,
        "listening": discord.Activity,
        "watching": discord.Activity
    }

    if status.lower() not in status_mapping:
        await interaction.response.send_message("Statut invalide, choisissez parmi: online, idle, dnd, invisible.", ephemeral=True)
        return

    bot_status = status_mapping[status.lower()]

    # Pour une activité de type "watching", "listening", ou "streaming", on peut définir un nom
    if activity and activity.lower() in activity_mapping:
        activity_type = activity_mapping[activity.lower()]
        activity_instance = activity_type(name="Je suis cool !")  # Exemple d'activité
        await bot.change_presence(status=bot_status, activity=activity_instance)
        await interaction.response.send_message(f"Statut changé en {status} avec activité '{activity}'.", ephemeral=True)
    else:
        await bot.change_presence(status=bot_status)
        await interaction.response.send_message(f"Statut changé en {status}.", ephemeral=True)

# ======================
# Démarrer le bot
# ======================

bot.run(TOKEN)
