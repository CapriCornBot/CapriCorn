import discord
from discord.ext import commands
from client.ExtendedClient import ExtendedClient as Client


class SettingsCog(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot

    @commands.slash_command(name="settings")
    async def settings(self, ctx: discord.ApplicationContext, key: discord.Option(str, "Settings key")):
        settings = self.bot.settings.getSetting(ctx.guild.id, key)
        if settings is None:
            await ctx.interaction.response.send_modal(SettingsCog.SettingsModal(self.bot, key))
        else:
            await ctx.interaction.response.send_modal(SettingsCog.SettingsModal(self.bot, key, settings))

    class SettingsModal(discord.ui.Modal):
        def __init__(self, bot: Client,  key: str, value: str = None, *args, **kwargs):
            self.bot = bot
            self.key = key
            self.value = value
            super().__init__(title=f"Edit '{key}'", *args, **kwargs)
            self.add_item(discord.ui.InputText(label=f"Key", value=self.key))
            self.add_item(discord.ui.InputText(label="Value", value=self.value, placeholder="Setting Value"))

        async def callback(self, interaction: discord.Interaction):
            if self.children[0].value.lower() != self.key:
                self.bot.settings.setSettings(interaction.guild.id, self.key, None)

            self.bot.settings.setSettings(interaction.guild.id, self.children[0].value.lower(), self.children[1].value)
            await interaction.response.send_message(f"Set '{self.children[0].value}' to '{self.children[1].value}'")
