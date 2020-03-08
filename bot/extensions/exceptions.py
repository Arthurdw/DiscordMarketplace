import discord
from utils.data import get_prefix
from discord.ext import commands
from run import em


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.NotFound):
            return
        elif isinstance(error, (TypeError, commands.MissingRequiredArgument)):
            await ctx.send(**em(layout="error",
                                content=f"Missing argument(s) for the '{ctx.command.qualified_name}' command.\n"
                                        f"Use the command like this:\n{get_prefix(self.bot, ctx.message, True)}"
                                        f"{ctx.command.qualified_name} {' '.join(ctx.command.clean_params)}"))
        else:
            raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
