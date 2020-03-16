from discord.ext import commands, tasks
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
        write("")

    @tasks.loop(seconds=10)
    async def check_commit(self):
        print(read() != "")
        if read() != "":
            try:
                await self.push_commit(eval(read()))
                write("")
            except Exception as e:
                raise e

    async def push_commit(self, commit):
        title = f"[{commit['repo']}] {len(commit['commits'])} new commits."
        for channel in [self.bot.get_channel(channel_id) for channel_id in update_channels()]:
            await channel.send(**em(title=title, content=commit["changes"]))

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_commit.start()


def setup(bot):
    bot.add_cog(Updates(bot))
