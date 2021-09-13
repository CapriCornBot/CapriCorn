import asyncio
from operator import sub
import discord
from discord.ext import commands
from discord_ui import UI, SlashOption, SlashedSubCommand, SlashedCommand
from discord_ui.slash.types import SlashCommand, SlashSubcommand
from discord_ui.cogs import subslash_cog, slash_cog
import typing

class Info:
    version = "1.0.0"
    author = "CC Team"
    name = "Settings"
    description = "Einstellungen"
    dev_mode = True

class Settings(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.ui: UI = self.bot.ui

    @commands.command(name="test")
    async def settings(self, ctx, query = "123"):
        await ctx.reply(self.bot.mongodb.find_one("settings", {"test": query}))

    @commands.command(name="test_insert")
    async def test_insert(self, ctx, text: str = "123"):
        await ctx.reply(self.bot.mongodb.insert("settings", {"test": text}))

    @commands.command(name="test_delete")
    async def test_delete(self, ctx, text: str = "123"):
        await ctx.reply(self.bot.mongodb.delete("settings", {"test": text}))
    @commands.command(name="test_update")
    async def test_update(self, ctx, text: str = "123", text2 = "123"):
        await ctx.reply(self.bot.mongodb.update("settings", {"test": text}, {"test": text2}))

    @slash_cog("testing", guild_ids=[883465097283002439])
    async def slash_cog_test(self, ctx):
        await ctx.defer()
        await asyncio.sleep(6)
        await ctx.respond("HeyGuys")

    @commands.Cog.listener("on_ready")
    async def on_ready(self): 
        await self.add_commands_to_guild()
        self.bot.db.execute("CREATE TABLE IF NOT EXISTS cc_settings( `id` INT NOT NULL ,`guild_id` TEXT NOT NULL, `last_updated` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , `welcome_channel` TEXT NULL , `welcome_embed` TEXT NULL ) ENGINE = InnoDB;")
        #await self.ui.slash.sync_commands(True)

    async def handle_slash_settings_1(ctx, nachricht: str):
        await ctx.respond("HeyGuys")
        pass
    
    @commands.Cog.listener("on_mysql_connected")
    async def on_mysql_connected(self):
        pass
    
    # @subslash_cog(["settings", "welcome"], "message", guild_ids=[883465097283002439], options=[SlashOption(str, "Nachricht", "Welcome message", True)])
    # async def handle_slash_settings_1(ctx, nachricht: str):
    #     await ctx.respond("HeyGuys")
    #     pass

    @commands.Cog.listener("on_slash_command")
    async def on_slash_command(self, ctx: typing.Union[SlashedCommand, SlashedSubCommand]):
        self.bot.logger.info(f"Trigger Slash Command")
        self.bot.logger.info(type(ctx))
        if hasattr(ctx, "base_names"):
            self.bot.logger.info(ctx.base_names)
            if "settings" == ctx.base_names[0]:
                if "welcome" == ctx.base_names[1]:
                    pass
            if ctx.base_names == ["settings", "welcome"]:
                await ctx.respond("Test")
            if ctx.base_names == ["settings", "vote"]:
                if ctx.name == "vote":
                    await ctx.respond("Testing")
        

    async def add_commands_to_guild(self):
        pass
        #guilds = self.bot.fetch_guilds(limit=None)
        #self.ui.slash.subcommand(["settings", "welcome"], "message", guild_ids=[883465097283002439], options=[SlashOption(str, "Nachricht", "Welcome message", True)])(self.handle_slash_settings_1)
        #self.ui.slash.subcommand(["settings", "welcome"], "message", guild_ids=[883465097283002439], options=[SlashOption(str, "Nachricht", "Welcome message", True)])(self.handle_slash_settings_1)
        self.ui.slash.add_subcommand(["settings", "vote"], "link", guild_ids=[883465097283002439], options=[SlashOption(str, "vote_link", "Vote link", True)])
def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))