import discord
from discord.ext import commands
import os
import asyncio
import time
from discord import app_commands
import subprocess
import sys
import ast

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def install_package(package_name):
    """Automatically installs a package if it is missing."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed package: {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install package: {package_name} - {e}")

def get_imports_from_file(filepath):
    with open(filepath, "r") as file:
        tree = ast.parse(file.read(), filename=filepath)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    return imports

async def load_commands():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            cog_name = f"commands.{filename[:-3]}"
            try:
                filepath = os.path.join("./commands", filename)
                required_modules = get_imports_from_file(filepath)
                for module in required_modules:
                    try:
                        __import__(module)
                    except ImportError:
                        await install_package(module)

                await bot.load_extension(cog_name)
                print(f"Loaded: {cog_name}")
            except Exception as e:
                print(f"Failed to load {cog_name}: {e}")

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")
    await load_commands()
    await bot.tree.sync()
    print("Slash commands synced!")

bot.run("")
