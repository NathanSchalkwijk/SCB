import discord
from discord.ext import commands

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='status')
    @commands.has_permissions(administrator=True)
    async def set_status(self, ctx, type: str = None, *, message: str = None):
        """
        Change the bot's status.
        Usage: !status <type> <message>
        Types: playing, streaming, listening, watching
        Use !status clear to reset status.
        """
        activity_types = {
            "playing": discord.Game(name=message),
            "streaming": discord.Streaming(name=message, url="https://www.twitch.tv/example"),
            "listening": discord.Activity(type=discord.ActivityType.listening, name=message),
            "watching": discord.Activity(type=discord.ActivityType.watching, name=message)
        }
        
        if type is None or type.lower() == "clear":
            await self.bot.change_presence(activity=None)
            await ctx.send("✅ Status cleared.")
        elif type.lower() in activity_types:
            await self.bot.change_presence(activity=activity_types[type.lower()])
            await ctx.send(f"✅ Status updated to {type.capitalize()} {message}")
        else:
            await ctx.send("❌ Invalid type! Choose from: playing, streaming, listening, watching or use !status clear.")

async def setup(bot):
    await bot.add_cog(StatusCog(bot))
