import configparser
import glob
import os
import sys
from settings.layouts import layout
from discord.ext import commands
from utils import data
# from util.core import GitHub
from BeatPy.discord import formatter

clear, back_slash = "clear", "/"
if os.name == "nt":
    clear, back_slash = "cls", "\\"

os.system(clear)

config = configparser.ConfigParser()
token = configparser.ConfigParser()
config.read("settings/config.cfg")
token.read("settings/token.cfg")
setup = formatter.Embed(layout_set=layout, footer=True, timestamp=True,
                        footer_message=config["EMBED"]["message"], footer_icon=config["EMBED"]["icon"])
em = setup.create


class Manager(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=data.get_prefix,
                         description=config["UTIL"]["desc"],
                         case_insensitive=True,
                         help_attrs=dict(hidden=True))
        # Display and load extensions!)
        for extension in glob.glob("extensions/*.py"):
            print("\b" + extension.replace("extensions" + back_slash, "")[:-3] + ": Starting", end='')
            sys.stdout.flush()
            self.load_extension(extension.replace(back_slash, ".")[:-3])
            print("\r", "\b" + extension.replace("extensions" + back_slash, "")[:-3] + ": Ready     ")
            sys.stdout.flush()

    async def on_ready(self):
        print('\n*-* *-* *-* *-* *-* *-* *-* *-*')
        print('*-* Logged in as:           *-*')
        print(f'*-* Name: {self.user.name}#{self.user.discriminator}      *-*')
        print(f'*-* ID: {self.user.id}  *-*')
        # print(f'*-* Version: {GitHub.version()}        *-*')
        print('*-* *-* *-* *-* *-* *-* *-* *-*\n')

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    def run(self):
        super().run(token["TOKEN"]["token"], reconnect=True)


if __name__ == '__main__':
    Manager().run()
