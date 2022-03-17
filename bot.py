# Programmed by Redstonezockt
# Programmed by Fluffeliger

from client.ExtendedClient import ExtendedClient as Client
from os import getenv
from dotenv import load_dotenv
import discord
import logging
from cog.settings import SettingsCog
load_dotenv()
TOKEN = getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = Client(auto_sync_commands=False, command_prefix="cc!", intents=intents)


@client.listen("on_ready")
async def on_ready():
    client.logger.info("Ready! Pterodactyl")
    client.logger.info(f"Logged in as {client.user}")

    client.locale.getString('en-US', 'test')


client.add_cog(SettingsCog(client))
client.run(TOKEN)
