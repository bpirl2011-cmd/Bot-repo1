import os
import discord
from discord.ext import commands
from flask import Flask, jsonify, request
import threading

# 1. Setup Command Queue Pipeline
app = Flask('')
current_command = "none"
target_argument = ""

@app.route('/')
def home(): 
    return "Command Router Active"

# Roblox calls this endpoint to check if Discord sent a command
@app.route('/getcommand', methods=['GET'])
def get_command():
    global current_command, target_argument
    data = {"command": current_command, "arg": target_argument}
    current_command = "none" # Reset command after Roblox reads it
    target_argument = ""
    return jsonify(data)

def run(): 
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run).start()

# 2. Discord Bot Engine
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Command Router Online as {bot.user.name}")

@bot.command()
async def rejoin(ctx):
    global current_command
    current_command = "rejoin"
    await ctx.send("🔄 Sending Rejoin command to Roblox...")

@bot.command()
async def Goto(ctx, name: str):
    global current_command, target_argument
    current_command = "goto"
    target_argument = name
    await ctx.send(f"🚀 Teleporting bot to player: **{name}**")

token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
