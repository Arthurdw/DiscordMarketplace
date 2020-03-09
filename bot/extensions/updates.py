import discord
from discord.ext import commands
from run import em


class Updates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Updates(bot))
