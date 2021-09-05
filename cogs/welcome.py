import discord
from discord.ext import commands

from discord_ui.cogs import subslash_cog
from discord_ui import UI


class Info:
    version = "1.0.0"
    author = "CC Team"
    name = "Welcome"
    description = "Welcome Messages"
    dev_mode = True

class Welcome(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.welcome_message = "Wilkommen %user%"
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.bot.fetch_channel("883465097283002443").send(self.welcome_message.replace("%user%", member.mention))

    @commands.command("cog_wlc_test")
    async def test(self, ctx):
        await self.bot.dispatch("member_join", ctx.author)

    @subslash_cog(base_names="set", guild_ids=[883465097283002439])
    async def welcome_message(self, ctx, msg: str):
        self.welcome_message = msg
        await ctx.send("Die Nachricht wurde geändert")
        self.bot.dispatch("member_join", ctx.author)

def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))