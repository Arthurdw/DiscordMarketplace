from discord.ext import commands
from run import em
from utils.data import admins, update_channels


class Fetch:
    def __init__(self):
        self.general = None

    def setup(self, obj):
        self.general = obj


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current = None

    async def push_commit(self, commit):
        title = f"[{commit['repo']}] {len(commit['commits'])} new commits."
        for channel in [self.bot.get_channel(channel_id) for channel_id in update_channels()]:
            await channel.send(**em(title=title, content=commit["changes"]))

    @staticmethod
    def user_content(ctx, message):
        if not (ctx.author.id in admins() or ctx.author.guild_permissions.manage_messages):
            message = ctx.message.clean_content
        return message

    @commands.command()
    async def test(self, ctx):
        await general.general.push_commit({"repo": "testWebhookRepo", "count": 1, "commits": [{"author": "Arthurdw", "author_avatar": "https://avatars0.githubusercontent.com/u/38541241?v=4", "author_url": "https://github.com/Arthurdw", "message ": ["Update aa.py "], "time ": "datetime.datetime(2020, 3, 9, 21, 12, 37)"}], "changes": "Updated `1` files:\n**Modified** (`1`): `aa.py`"})

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(self.user_content(ctx, message))

    @commands.command()
    async def embed(self, ctx, *, message):
        await ctx.send(**em(self.user_content(ctx, message),
                            footer_message=f"Send by {ctx.author}", footer_icon=ctx.author.avatar_url, timestamp=False))


general = Fetch()


def setup(bot):
    general.setup(General(bot))
    bot.add_cog(General(bot))
