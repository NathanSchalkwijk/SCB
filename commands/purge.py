import discord
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: str):
        if amount.lower() == "all":
            amount = 999999
        else:
            try:
                amount = int(amount)
                if amount <= 0:
                    return await ctx.send("Please specify a number greater than 0.", delete_after=2)
            except ValueError:
                return await ctx.send("Please provide a valid number of messages to delete.", delete_after=2)

        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Deleted {len(deleted)-1} messages.", delete_after=2)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.", delete_after=2)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I need the `Manage Messages` permission to do that.", delete_after=2)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid number of messages to delete.", delete_after=2)
        else:
            await ctx.send("An error occurred.", delete_after=2)

async def setup(bot):
    await bot.add_cog(Purge(bot))
