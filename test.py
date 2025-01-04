import discord
from discord.ext import commands
import tkinter as tk
from tkinter import messagebox

class DiscordBot(commands.Bot):
    def __init__(self, command_prefix="!"):
        intents = discord.Intents.default()
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        print(f"Bot {self.user} connecté.")

bot = DiscordBot()

# Fonction pour changer le statut du bot
def set_bot_status(status, activity=None):
    try:
        if status == "online":
            status_enum = discord.Status.online
        elif status == "idle":
            status_enum = discord.Status.idle
        elif status == "dnd":
            status_enum = discord.Status.dnd
        elif status == "invisible":
            status_enum = discord.Status.invisible
        else:
            raise ValueError("Statut invalide")

        if activity:
            activity_enum = discord.Game(name=activity)
            bot.change_presence(status=status_enum, activity=activity_enum)
        else:
            bot.change_presence(status=status_enum)

        messagebox.showinfo("Succès", f"Statut du bot changé en {status}.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")

# Fonction pour fermer le bot
def stop_bot():
    bot.close()
    window.quit()

# Création de la fenêtre Tkinter
window = tk.Tk()
window.title("Contrôle du Bot Discord")

# Fonction pour mettre à jour le statut
def update_status():
    status = status_var.get()
    activity = activity_entry.get()
    set_bot_status(status, activity)

# Choix du statut
status_var = tk.StringVar(value="online")
status_label = tk.Label(window, text="Statut du bot :")
status_label.pack()

status_online = tk.Radiobutton(window, text="Online", variable=status_var, value="online")
status_online.pack()

status_idle = tk.Radiobutton(window, text="Idle", variable=status_var, value="idle")
status_idle.pack()

status_dnd = tk.Radiobutton(window, text="Do Not Disturb", variable=status_var, value="dnd")
status_dnd.pack()

status_invisible = tk.Radiobutton(window, text="Invisible", variable=status_var, value="invisible")
status_invisible.pack()

# Activité du bot
activity_label = tk.Label(window, text="Activité du bot (facultatif) :")
activity_label.pack()

activity_entry = tk.Entry(window)
activity_entry.pack()

# Bouton pour mettre à jour le statut
update_button = tk.Button(window, text="Mettre à jour le statut", command=update_status)
update_button.pack()

# Bouton pour fermer le bot
stop_button = tk.Button(window, text="Arrêter le bot", command=stop_bot)
stop_button.pack()

# Lancer la fenêtre Tkinter
window.mainloop()

# Démarrer le bot Discord (dans un thread séparé ou async)
bot.run("TOKEN")
