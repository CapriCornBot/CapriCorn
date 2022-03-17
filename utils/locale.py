from typing import overload
import json


class Locale:
    def __init__(self, bot):
        from client.ExtendedClient import ExtendedClient as Client
        self.bot: Client = bot
        pass

    def getLocale(self, guild_id) -> str:
        return self.bot.settings.getSetting(guild_id, 'locale', 'en-US')

    def setLocale(self, guild_id, language_code) -> tuple[str, str]:
        self.bot.settings.setSetting(guild_id, 'locale', language_code)
        return guild_id, language_code

    @overload
    def getString(self, guild_id: int, key: str) -> str:
        ...

    @overload
    def getString(self, language_code: str, key: str) -> str:
        ...

    def getString(self, input1, key) -> str:
        locales = ["en-US"]

        locale = None
        if isinstance(input1, int):
            locale = self.getLocale(input1)
        elif isinstance(input1, str):
            locale = input1

        if locale not in locales:
            return "ERR: LANGUAGE_NOT_SUPPORTED"

        s = json.load(open(f'lang/{locale}.json'))

        print(s)

        return "None"

    def parseEmbed(self, locale_code, category, embed_name):
        # CATEGORY - EMBEDS - EMBEDNAME
        # self.bot.db.
        pass
