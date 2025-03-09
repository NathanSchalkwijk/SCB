import discord
from discord.ext import commands
import os
import asyncio
import time
import subprocess
import sys
import ast
import importlib.util

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def is_package_installed(package_name):
    return importlib.util.find_spec(package_name) is not None

def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, '--break-system-packages'])
        print(f"Successfully installed package: {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install package: {package_name} - {e}")

def get_imports_from_file(filepath):
    with open(filepath, "r") as file:
        tree = ast.parse(file.read(), filename=filepath)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0]) 
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0]) 
    
    return imports

async def load_commands():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            cog_name = f"commands.{filename[:-3]}"
            try:
                filepath = os.path.join("./commands", filename)
                required_modules = get_imports_from_file(filepath)
                third_party_modules = {mod for mod in required_modules if importlib.util.find_spec(mod) is None}
                for module in third_party_modules:
                    if not is_package_installed(module):
                        install_package(module)
                
                await bot.load_extension(cog_name)
                print(f"Loaded: {cog_name}")
            except Exception as e:
                print(f"Failed to load {cog_name}: {e}")

@bot.command(name="reload")
async def reload(ctx, cog_name: str):
    try:
        try:
            await bot.unload_extension(f"commands.{cog_name}")
        except Exception:
            pass
        filepath = os.path.join("./commands", f"{cog_name}.py")
        required_modules = get_imports_from_file(filepath)
        third_party_modules = {mod for mod in required_modules if importlib.util.find_spec(mod) is None}
        for module in third_party_modules:
            if not is_package_installed(module):
                install_package(module)    
        await bot.load_extension(f"commands.{cog_name}")
        await ctx.send(f"Cog '{cog_name}' has been reloaded!")
    except Exception as e:
        await ctx.send(f"Error reloading cog '{cog_name}': {e}")

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")
    await load_commands()
    await bot.tree.sync()
    print("Slash commands synced!")

bot.run("")
