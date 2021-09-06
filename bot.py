import asyncio
from utils.database import Database
import discord
from discord.ext import commands, tasks
from discord_ui import UI
import os
from dotenv import load_dotenv
from cogs.load import load_cogs, middle_text
from utils import logger
from config import config
import logging
import threading

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BOT_NAME = config.bot_name

log = logging.getLogger(BOT_NAME)
client = commands.Bot(command_prefix='cc!')
client.ui = UI(client, slash_options={'auto_sync': False, "sync_on_cog": True})
client.http.token = DISCORD_TOKEN
client.logger = logger.register_logger("bot.log", BOT_NAME)
client.db = Database(client)
client.db.connect()


@client.listen('on_connect')
async def on_connect():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"Starting Up..."))
    log.info("Verbindung mit der Discord API Hergestellt!")
    log.info(
        "╔═════════════════╦══════════════════════════════════════════════════════════════════════════════════════╗"
    )
    log.info(f"║ {middle_text('Name', 15)} ║ {middle_text('Wert', 84)} ║")
    log.info(
        "╠═════════════════╬══════════════════════════════════════════════════════════════════════════════════════╣"
    )
    log.info(f"║ {middle_text('Name', 15)} ║ {middle_text(f'{client.user}', 84)} ║")
    log.info(f"║ {middle_text('ID', 15)} ║ {middle_text(f'{client.user.id}', 84)} ║")
    log.info(
        f"║ {middle_text('User Agent', 15)} ║ {middle_text(f'{client.http.user_agent}', 84)} ║"
    )
    log.info(
        f"║ {middle_text('Discord Version', 15)} ║ {middle_text(f'{discord.__version__}', 84)} ║"
    )
    log.info(
        "╚═════════════════╩══════════════════════════════════════════════════════════════════════════════════════╝"
    )
    #client.loop.create_task(client.www.app.run(debug=True, use_reloader=False))
    #client.www.thread.start()

@client.listen('on_ready')
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"v0.1 | capricornbot.de"))

load_cogs(client)

client.run(DISCORD_TOKEN)