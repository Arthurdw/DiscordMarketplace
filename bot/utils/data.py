import configparser
config = configparser.ConfigParser()
config.read("settings/config.cfg")


def admins():
    """Returns an array of admins. (Bypass every check)"""
    return [int(name.strip()) for name in str(config["UTIL"]["admins"]).split(",")]


def get_prefix(bot, message, main=False):
    """Retrieves the current guild its bot prefix."""
    prefix = "!"
    mentions = ['<@686285057782055083> ', '<@!686285057782055083> ', '<@686285057782055083>', '<@!686285057782055083>']
    if not main:
        mentions.append(prefix)
    return prefix if main else mentions


def update_channels():
    """Returns the channels which are signed up to receive update notifications."""
    return [685811186091950254]
