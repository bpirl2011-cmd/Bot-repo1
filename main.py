import os
import discord
from discord.ext import commands
from flask import Flask, jsonify, request
import threading

app = Flask('')
current_command = "none"
target_argument = ""
remaining_loops = 0
discord_channel_id = 0

@app.route('/')
def home(): 
    return "Killswitch Router Active"

@app.route('/getcommand', methods=['GET'])
def get_command():
    global current_command, target_argument, remaining_loops, bot, discord_channel_id
    
    # If the user typed !stop, tell Roblox to halt and clear everything
    if current_command == "stop":
        current_command = "none"
        remaining_loops = 0
        target_argument = ""
        return jsonify({"command": "stop", "arg": "", "loops": 0})
        
    if remaining_loops > 0:
        data = {"command": "start_loop", "arg": target_argument, "loops": remaining_loops}
        remaining_loops -= 1
        return jsonify(data)
    
    if remaining_loops == 0 and current_command == "running":
        current_command = "none"
        if bot and discord_channel_id:
            channel = bot.get_channel(discord_channel_id)
            if channel:
                bot.loop.create_task(channel.send(f"✅ **Loop Complete!** Bot has finished all loops."))
    
    return jsonify({"command": "none", "arg": "", "loops": 0})

def run(): 
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run).start()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Router Online as {bot.user.name}")

@bot.command()
async def start(ctx, *, args: str):
    global current_command, target_argument, remaining_loops, discord_channel_id
    discord_channel_id = ctx.channel.id
    parts = args.split("=")
    if len(parts) >= 2:
        target_argument = parts[0].strip()
        try:
            remaining_loops = int(parts[1].strip())
            current_command = "running"
            await ctx.send(f"⚔️ **Loop Started!** Targeting `{target_argument}` for `{remaining_loops}` loops.")
        except ValueError:
            await ctx.send("❌ Invalid number.")
    else:
        await ctx.send("❌ Use: !start=Name=100")

@bot.command()
async def stop(ctx):
    global current_command, remaining_loops, target_argument
    current_command = "stop"
    remaining_loops = 0
    target_argument = ""
    await ctx.send("🛑 **STOP COMMAND SENT.** Resetting bot to Prisoner and rejoining to halt auto-execute.")

token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
