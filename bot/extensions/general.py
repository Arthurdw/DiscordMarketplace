from discord.ext import commands
from run import em
from utils.data import admins


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def user_content(ctx, message):
        if not (ctx.author.id in admins() or ctx.author.guild_permissions.manage_messages):
            message = ctx.message.clean_content
        return message

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(self.user_content(ctx, message))

    @commands.command()
    async def embed(self, ctx, *, message):
        await ctx.send(**em(self.user_content(ctx, message),
                            footer_message=f"Send by {ctx.author}", footer_icon=ctx.author.avatar_url, timestamp=False))


def setup(bot):
    bot.add_cog(General(bot))
