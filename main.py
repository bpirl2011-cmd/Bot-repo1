import os
import discord
from discord.ext import commands
from flask import Flask
import threading

# 1. Keep-Alive Web Server for Render
app = Flask('')
@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server).start()

# 2. Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! The bot is online and working.")

# 3. Start the Bot using the Token from Render
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
