class Settings:
    def __init__(self, bot) -> None:
        from client.ExtendedClient import ExtendedClient
        self.bot: ExtendedClient = bot
        super().__init__()

    def guildExists(self, guild_id) -> bool:
        row = self.bot.db.find_one("bot_settings", {"guild_id": f"{guild_id}"})
        if row is None:
            return False
        return True

    def getSetting(self, guild_id, key, default=None):
        row = self.bot.db.find_one("bot_settings", {"guild_id": f"{guild_id}"})
        if row is None:
            return default
        if key in row:
            return row[key]
        return default

    def setSettings(self, guild_id, key, value):
        if not self.guildExists(guild_id):
            self.bot.db.insert_one("bot_settings", {"guild_id": f"{guild_id}"})
        if(value is None):
            self.bot.db.update_one("bot_settings", {"guild_id": f"{guild_id}"}, {"$unset": {key: ""}})
        else:
            self.bot.db.update_one("bot_settings", {"guild_id": f"{guild_id}"}, {'$set': {key: value}})

