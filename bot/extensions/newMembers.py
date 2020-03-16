import discord
from run import em, formatter
from discord.ext import commands
from extensions.logger import Logger
from configparser import ConfigParser

config = ConfigParser()
config.read("settings/config.cfg")

field = formatter.Field


class NewMembers(commands.Cog):
    server = config["GENERAL"]["main-server"]
    verify_channel = config["GENERAL"]["verify"]
    join_roles = [role.strip() for role in config["GENERAL"]["join-roles"].split(",")]
    verify_roles = [role.strip() for role in config["GENERAL"]["verify-roles"].split(",")]
    main_server = None
    join_leave = None

    def __init__(self, bot):
        self.bot = bot
        self.log = Logger(bot)

    async def send_join_leave(self, member, join=True):
        if self.main_server is None and self.join_leave is None:
            return False
        if member.bot and join:
            await member.add_roles(self.main_server.get_role(688802297500794900))
            await self.log.send_bot_add(member)
            return False
        await self.join_leave.send(member.mention if join else "",
                                   **em(config["GENERAL"]["welcomeMSG" if join else "leaveMSG"].format(member=member,
                                                                                                       nl="\n",
                                                                                                       verify=self.verify_channel)))
        return True

    @commands.is_owner()
    @commands.command(name="rules")
    async def rules(self, ctx):
        await ctx.send(**em(content="Hello, newlings!\nFirst of all welcome to the official `Discord Marketplace` server!\n"
                                    "This server will provide support for any questions you might have about the platform.\n"
                                    "If you want to add a bot/server or ad of your own, it’s highly recommended to be in this discord server.\n"
                                    "To make sure nothing happens, please read  ‘__**Information**__’ and ‘__**Rules**__’!",
                            fields=[field("Information", "Breaking any of these rules may result in a punishment.\n"
                                                         "You should always listen to the role above you. *(`Member` < `Management` < `Senior Management` < `Founder`)*", False),
                                    field("Rules", "**#1** | Don’t ask for free stuff!\n"
                                                   "**#2** | Follow the channel guidelines!\n"
                                                   "**#3** | Do not harras/insult other members! (includes staff)\n"
                                                   "**#4** | No toxicity is allowed!\n"
                                                   "**#5** | No swearing!\n"
                                                   "**#6** | No kind of NSFW content is allowed!\n"
                                                   "**#7** | Only speak English or Dutch in <#688853503875088576>, if you want to speak another language go to <#688853522330026031>!\n"
                                                   "**#8** | No chat/voice spamming/caps/zalgo is allowed!\n"
                                                   "**#9** | No political arguments/discussions.\n"
                                                   "**#10** | Listen to staff. (think the staff is abusing this? DM <@232182858251239424>)", False)],
                            footer_message="Discord Marketplace | Information & Rules",
                            timestamp=False))

    @commands.Cog.listener()
    async def on_ready(self):
        self.main_server = self.bot.get_guild(int(self.server))
        self.join_leave = self.bot.get_channel(int(config["GENERAL"]["join-leave"]))
        self.verify_roles = [self.main_server.get_role(int(role)) for role in self.verify_roles]
        self.join_roles = [self.main_server.get_role(int(role)) for role in self.join_roles]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.main_server is None:
            return
        if payload.guild_id == int(self.server) and payload.channel_id == int(self.verify_channel):
            await payload.member.remove_roles(*self.verify_roles)
            await self.log.send_verified(payload.member.id)
            await payload.member.send(**em(f"You successfully verified yourself in `{self.main_server.name}`."))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.send_join_leave(member):
            await member.add_roles(*self.verify_roles)
            await member.add_roles(*self.join_roles)
            try:
                await member.send(**em(f"Thanks for joining `{self.main_server.name}`, have a great time here!"))
            except discord.errors.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.send_join_leave(member, False)


def setup(bot):
    bot.add_cog(NewMembers(bot))
