import discord
import asyncio
from run import em, formatter
from extensions.logger import Log, Logger
from discord.ext import commands
from configparser import ConfigParser

config = ConfigParser()
config.read("settings/config.cfg")

field = formatter.Field


class Moderation(commands.Cog):
    founder_role_id = int(config["UTIL"]["founder-role"])
    senior_management_role_id = int(config["UTIL"]["senior-management-role"])
    management_role_id = int(config["UTIL"]["management-role"])
    all_perms = [founder_role_id, senior_management_role_id, management_role_id]

    def __init__(self, bot):
        self.bot = bot
        self.log = Logger(self.bot)

    @staticmethod
    async def checks(ctx, member, command):
        if member is None:
            await ctx.send(**em(f"Please specify a member you want to {command}!"))
            return False
        elif member == ctx.author:
            await ctx.send(**em(f"You cant {command} yourself!"))
            return False
        return True

    @commands.command(name="kick")
    @commands.has_any_role(*all_perms)
    async def kick(self, ctx, member: discord.Member = None, *, reason="Undefined"):
        role_ids = [role.id for role in member.roles]
        if 688802497006927924 in role_ids:
            return await ctx.send(**em("You can't kick server bots!"))
        if await self.checks(ctx, member, "kick"):
            if [i for i in role_ids if i in self.all_perms]:
                return await ctx.send(**em("This user is currently in the management team.\n"
                                           "If you would like to kick/remove this user from the server the demotion protocol should be used.\n"
                                           "If you are a member of the management team you are unable to do this and if you have something against a member from the management team please contact a member of the senior management team."))
            msg = await ctx.send(**em(content=f"Are you sure you want to kick {member.mention}?\n"
                                              f"Reason for kick:\nReason:\n```\n{reason.strip()}\n```",
                                      fields=[field(f"{member}'s information:",
                                                    f"User roles: {', '.join(sorted([role.mention for role in member.roles if role.name != '@everyone']))}")]))
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            def check(_reaction, _user):
                return _user == ctx.author and (str(_reaction.emoji) == "✅" or str(_reaction.emoji) == "❌")
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                try:
                    await msg.edit(**em("You didn't react or to late. *(60s+)*"))
                except discord.errors.NotFound:
                    await ctx.send(**em("You didn't react or to late. *(60s+)*"))
                await msg.clear_reactions()
            else:
                if str(reaction) == "✅":
                    if not member.bot:
                        try:
                            await member.send(**em(f"Hey {member.mention}!\n"
                                                   f"Unfortunately you have been kicked from `{ctx.guild.name}`.\n"
                                                   f"You got kicked by {ctx.author.mention} [{ctx.author.top_role.name}] (`{ctx.author.id}`).\n"
                                                   f"The reason for the kick was the following:\n```\n{reason.strip()}\n```"))
                        except discord.errors.Forbidden:
                            pass
                    await member.kick(reason=reason)
                    log_obj = Log('kick', member,  ctx.author, reason.strip())
                    log = await self.log.send_log(log_obj)
                    log_obj.id = str(log.id)
                    await self.log.edit_log(log, log_obj)
                    try:
                        await msg.edit(**em(f"Successfully kicked {member}!\nReason:\n```\n{reason.strip()}\n```"))
                    except discord.errors.NotFound:
                        await ctx.send(**em(f"Successfully kicked {member}!\nReason:\n```\n{reason.strip()}\n```"))
                    await msg.clear_reactions()
                else:
                    try:
                        await msg.edit(**em("Stopped the kicking protocol!"))
                    except discord.errors.NotFound:
                        await ctx.send(**em("Stopped the kicking protocol!"))
                    await msg.clear_reactions()


def setup(bot):
    bot.add_cog(Moderation(bot))
