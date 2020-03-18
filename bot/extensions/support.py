import discord
from run import em, formatter
from discord.ext import commands
from utils.data import get_support
from difflib import get_close_matches
from configparser import ConfigParser

config = ConfigParser()
config.read("settings/config.cfg")
field = formatter.Field


class Support(commands.Cog):
    server = config["GENERAL"]["main-server"]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id == int(config["GENERAL"]["main-server"]):
            async def check_leave():
                if before.channel is not None and before.channel.category.id == int(config["SUPPORT"]["support-cat"]):
                    if before.channel.id != int(config["SUPPORT"]["support-vc"]):
                        if len(before.channel.members) == 0:
                            await before.channel.delete(reason="Channel is empty!")
            if after.channel is not None:
                await check_leave()
                if after.channel.id == int(config["SUPPORT"]["support-vc"]):
                    channel = await member.guild.create_voice_channel(name=f"Support: {member.name}",
                                                                      category=after.channel.category,
                                                                      reason=f"Voice Support channel for {member}",
                                                                      position=1, topic="Voice Support channel")
                    await channel.set_permissions(member.guild.default_role, connect=False)
                    await channel.set_permissions(member.guild.default_role, connect=False)
                    await member.move_to(channel, reason="Voice Support")
            else:
                await check_leave()

    @commands.command()
    @commands.has_any_role(int(config["UTIL"]["management-role"]))
    async def trigger(self, ctx, *, trigger: str):
        """Triggers a support keyword."""
        try:
            response = get_support()[trigger]
            await ctx.send(**em(response["response"]))
        except KeyError:
            closest = get_close_matches(trigger, [str(item).lower() for item in get_support()])
            extra = f"Did you mean `{'`, `'.join(closest)}`?" if closest else ""
            await ctx.send(**em(f"Did not find any matching trigger keys.\n{extra}"))

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id == int(config["SUPPORT"]["support-c"]):
            ctx = await self.bot.get_context(message)
            if not ctx.valid:
                keywords = get_support()
                for cat in keywords:
                    msg = em(fields=[field("Automated response:", keywords[cat]["response"], False)],
                             content=f"This is an auto response.\nIf this isn't right we're sorry.")
                    for word in message.content.lower().split(" "):
                        found = get_close_matches(word, keywords[cat]["keywords"])
                        if found:
                            return await ctx.send(ctx.author.mention, **msg)
                    for keyword in keywords[cat]["keywords"]:
                        if keyword in str(message.content).lower():
                            return await ctx.send(ctx.author.mention, **msg)

    @commands.Cog.listener()
    async def on_ready(self):
        self.server = self.bot.get_guild(int(self.server))


def setup(bot):
    bot.add_cog(Support(bot))
