import discord
from discord.ext import commands
from run import em
from utils.data import update_channels


class Fetch:
    def __init__(self):
        self.update = None

    def setup(self, obj):
        self.update = obj


class Updates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def push_commit(self, commit):
        title = f"[{commit['repo']}] {len(commit['commits'])} new commits."
        for channel in [self.bot.get_channel(channel_id) for channel_id in update_channels()]:
            await channel.send(**em(title=title, content=commit["changes"]))
            
    @commands.command()
    async def test(self, ctx):
        await updates.update.push_commit({"repo": "testWebhookRepo", "count": 1, "commits": [{"author": "Arthurdw", "author_avatar": "https://avatars0.githubusercontent.com/u/38541241?v=4", "author_url": "https://github.com/Arthurdw", "message ": ["Update aa.py "], "time ": "datetime.datetime(2020, 3, 9, 21, 12, 37)"}], "changes": "Updated `1` files:\n**Modified** (`1`): `aa.py`"})

    

updates = Fetch()


def setup(bot):
    updates.setup(Updates(bot))
    bot.add_cog(Updates(bot))
