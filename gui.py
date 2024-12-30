import tkinter as tk
from tkinter import ttk
from bot import bot_status, bot_activity, stop_bot, run_bot
import discord
import asyncio
from threading import Thread

# Initialiser les options possibles
statuses = {
    "Online": discord.Status.online,
    "Idle": discord.Status.idle,
    "Do Not Disturb": discord.Status.dnd,
    "Invisible": discord.Status.invisible,
}

class BotControllerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Discord Controller")
        self.root.geometry("400x300")

        # Statut
        ttk.Label(root, text="Statut du Bot").pack(pady=10)
        self.status_var = tk.StringVar(value="Online")
        self.status_menu = ttk.Combobox(root, textvariable=self.status_var, values=list(statuses.keys()))
        self.status_menu.pack(pady=5)

        # Activité
        ttk.Label(root, text="Type d'activité").pack(pady=10)
        self.activity_var = tk.StringVar(value="Playing")
        self.activity_menu = ttk.Combobox(root, textvariable=self.activity_var, values=["Playing", "Streaming", "Listening", "Watching"])
        self.activity_menu.pack(pady=5)

        ttk.Label(root, text="Nom du jeu / activité").pack(pady=10)
        self.activity_name_var = tk.StringVar()
        self.activity_name_entry = ttk.Entry(root, textvariable=self.activity_name_var)
        self.activity_name_entry.pack(pady=5)

        # Boutons
        self.update_button = ttk.Button(root, text="Mettre à jour le statut", command=self.update_status)
        self.update_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Désactiver le Bot", command=self.stop_bot)
        self.stop_button.pack(pady=10)

    def update_status(self):
        global bot_status, bot_activity
        # Met à jour le statut
        bot_status = statuses[self.status_var.get()]

        # Met à jour l'activité
        activity_type = self.activity_var.get()
        activity_name = self.activity_name_var.get()
        if activity_type == "Playing":
            bot_activity = discord.Game(name=activity_name)
        elif activity_type == "Streaming":
            bot_activity = discord.Streaming(name=activity_name, url="https://twitch.tv/placeholder")
        elif activity_type == "Listening":
            bot_activity = discord.Activity(type=discord.ActivityType.listening, name=activity_name)
        elif activity_type == "Watching":
            bot_activity = discord.Activity(type=discord.ActivityType.watching, name=activity_name)
        print(f"Statut mis à jour : {self.status_var.get()} avec activité : {activity_name}")

    def stop_bot(self):
        asyncio.run(stop_bot())
        print("Bot désactivé")
        self.root.destroy()

# Lancer l'interface graphique et le bot
def main():
    root = tk.Tk()

    # Démarrer l'interface graphique
    gui = BotControllerGUI(root)

    # Lancer le bot dans un thread séparé
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
