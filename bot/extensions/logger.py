import discord
from run import config
from discord.ext import commands
from settings.layouts import logs
from BeatPy.discord import formatter

setup = formatter.Embed(layout_set=logs, footer=True, footer_message="Discord Marketplace Moderation", timestamp=True)
em = setup.create
field = formatter.Field


class Log:
    def __init__(self, layout, target, author, reason, log_id="000000000000000"):
        self.type = layout
        self.id = log_id
        self.target = target
        self.author = author
        self.reason = reason


class Logger(commands.Cog):
    log = None  # non type obj error

    def __init__(self, bot):
        self.bot = bot

    async def send_verified(self, user):
        if self.log is None:
            self.log = self.bot.get_channel(int(config["LOGGING"]["log-channel"]))
        await self.log.send(**em(f"<@{user}> (`{user}`) just got verified!", footer=False, timestamp=False))

    async def send_bot_add(self, user):
        if self.log is None:
            self.log = self.bot.get_channel(int(config["LOGGING"]["log-channel"]))
        await self.log.send(**em(f"BOT: <@{user.id}> (`{user.id}`) just got added!", footer=False, timestamp=False))

    @staticmethod
    async def send_data(action, data):
        return await action(**em(layout=data.type,
                                 content=f"{data.target.mention} got {data.type}{'ed' if data.type == 'kick' else ''} by {data.author.mention}!",
                                 fields=[field("Info:", f"Target: {data.target.mention} [{data.target.top_role.name}] (`{data.target.id}`)\n"
                                                        f"Moderator: {data.author.mention} [{data.author.top_role.name}] (`{data.author.id}`)\n"
                                                        f"Log ID: `{str(hex(int(data.id)))[2:]}`"),
                                         field("Reason", f"```\n{str(data.reason).strip()}\n```", False)],
                                 footer_icon=data.target.avatar_url))

    async def send_log(self, log: Log):
        if self.log is None:
            self.log = self.bot.get_channel(int(config["LOGGING"]["log-channel"]))
        return await self.send_data(self.log.send, log)

    async def edit_log(self, msg: discord.Message, log: Log):
        await self.send_data(msg.edit, log)

    @commands.Cog.listener()
    async def on_ready(self):
        self.log = self.bot.get_channel(int(config["LOGGING"]["log-channel"]))


def setup(bot):
    bot.add_cog(Logger(bot))
