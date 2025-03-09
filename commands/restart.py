import discord
import os
import sys
from discord.ext import commands

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="restart")
    async def restart(self, ctx):
        await ctx.send("Restarting bot...")
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

async def setup(bot):
    await bot.add_cog(Restart(bot))
