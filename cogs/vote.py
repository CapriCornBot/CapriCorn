import discord
from discord.ext import commands
from discord_ui import SlashedCommand
from discord_ui.cogs import slash_cog
from utils.locale import Locale
from utils.embeds import Embeds

class Info:
    version = "1.0.0"
    author = "CC Team"
    name = "Vote"
    description = "Vote Command / Handling"
    dev_mode = True

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @slash_cog("vote", guild_ids=[883465097283002439])
    async def vote_command(self, ctx: SlashedCommand):
        await ctx.defer(True)
        locale = Locale.from_guild_id(self.bot, ctx.guild_id)
        embeds = Embeds.from_locale(self.bot, locale)
        await ctx.respond(embed=embeds.info("Der Command geht :)"))

def setup(bot):
    bot.add_cog(Vote(bot))