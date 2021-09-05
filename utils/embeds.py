import discord
from utils.locale import Locale

class Embeds():
    def __init__(self, client,*, guild_id = None, locale = None):
        self.client = client
        if locale is None and guild_id is not None:
            self.locale = Locale.from_guild_id(client, guild_id)
        else:
            self.locale = locale
        pass
    
    @classmethod
    def from_guild_id(cls, client, guild_id):
        return cls(client, guild_id = guild_id)

    @classmethod
    def from_locale(cls,client,  locale):
        return cls(client, locale=locale)

    def fail(self, message):
        emb = discord.Embed(color=0xFF0000)
        emb.title = self.locale.get_message("global_embed_error_title")
        emb.description = message
        return emb
    
    def success(self, message):
        emb = discord.Embed(color=0x00FF00)
        emb.title = self.locale.get_message("global_embed_success_title")
        emb.description = message
        return emb

    def info(self, message):
        emb = discord.Embed(color=0x00FFFF)
        emb.title = self.locale.get_message("global_embed_info_title")
        emb.description = message
        return emb

