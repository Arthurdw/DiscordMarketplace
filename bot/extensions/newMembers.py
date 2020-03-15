import discord
from run import em
from configparser import ConfigParser
from discord.ext import commands

config = ConfigParser()
config.read("settings/config.cfg")


class NewMembers(commands.Cog):
    server = config["GENERAL"]["main-server"]
    verify_channel = config["GENERAL"]["verify"]
    join_roles = [role.strip() for role in config["GENERAL"]["join-roles"].split(",")]
    verify_roles = [role.strip() for role in config["GENERAL"]["verify-roles"].split(",")]
    main_server = None
    join_leave = None

    def __init__(self, bot):
        self.bot = bot

    async def send_join_leave(self, member, join=True):
        if self.main_server is None and self.join_leave is None:
            return
        await self.join_leave.send(member.mention if join else "",
                                   **em(config["GENERAL"]["welcomeMSG" if join else "leaveMSG"].format(member=member,
                                                                                                       nl="\n",
                                                                                                       verify=self.verify_channel)))

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
            await payload.member.add_roles(*self.verify_roles)
            await payload.member.send(**em(f"You successfully verified yourself in `{self.main_server.name}`."))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.send_join_leave(member)
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
