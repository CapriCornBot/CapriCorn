# Programmed by Redstonezockt
# Programmed by Fluffeliger

from discord.ext import commands
from abc import ABC
import discord
from discord.ext.commands import when_mentioned
from utils import logger
from utils.mongodb import MongoDB
from utils.settings import Settings
from utils.locale import Locale


class ExtendedClient(commands.Bot, ABC):

    db: MongoDB = None
    settings: Settings = None
    locale: Locale = None
    def __init__(self, command_prefix=when_mentioned, help_command=None, **options):
        super().__init__(command_prefix, help_command, **options)

        self.db = MongoDB()
        self.settings = Settings(self)
        self.locale = Locale(self)

    logger = logger.register_logger("capricorn.log", "CapriCorn")
    logger.info("Logger initialized")

