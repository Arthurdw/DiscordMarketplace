import discord
import datetime
from asyncio import sleep
from discord.ext import commands
from run import em
from utils.data import update_channels


def read():
    with open("utils/tempdata.txt") as f:
        data = f.read()
        f.close()
    return data


def write(data):
    with open("utils/tempdata.txt", "w") as f:
        f.truncate(0)
        f.write(data)
        f.close()


class Updates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.state = read()

    async def check_commit(self):
        while True:
            if self.state != read():
                await self.push_commit(eval(read()))
                self.state = read()
            await sleep(10)

    async def push_commit(self, commit):
        title = f"[{commit['repo']}] {len(commit['commits'])} new commits."
        for channel in [self.bot.get_channel(channel_id) for channel_id in update_channels()]:
            await channel.send(**em(title=title, content=commit["changes"]))

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.check_commit())


def setup(bot):
    bot.add_cog(Updates(bot))
