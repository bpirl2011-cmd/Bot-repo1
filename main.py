import os
import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import threading

# 1. Setup the Web Server to Listen to Roblox
app = Flask('')
bot_client = None  # To hold the bot instance safely

@app.route('/')
def home():
    return "Chat Logger is Active!"

@app.route('/log', methods=['POST'])
def log_chat():
    data = request.json
    player = data.get("player")
    message = data.get("message")
    channel_id = int(os.environ.get("CHANNEL_ID", 0)) # Set your channel ID in Render settings
    
    if bot_client and channel_id:
        channel = bot_client.get_channel(channel_id)
        if channel:
            # Sends message cleanly to your Discord server
            bot_client.loop.create_task(channel.send(f"💬 **{player}**: {message}"))
            return jsonify({"status": "success"}), 200
    return jsonify({"status": "failed"}), 400

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server).start()

# 2. Discord Bot System
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    global bot_client
    bot_client = bot
    print(f"Chat Logger Bot is Online as {bot.user.name}")

token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
