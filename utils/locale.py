import json
import logging
from config import config
log = logging.getLogger(config.bot_name)


class Locale:
    def __init__(self, locale) -> None:
        self.locale = locale
        self.locale_file = 'locale/' + locale + '.json'
        self.messages = {}
        try:
            self.load_messages()
        except:
            log.warning('Locale file not found: ' + self.locale_file)
            self.locale = "en"
            self.locale_file = 'locale/' + self.locale + '.json'
            self.load_messages()

    @classmethod
    def from_guild_id(cls, client, guild_id):
        client.db.execute("SELECT * FROM cc_settings WHERE guild_id=%s", [guild_id])
        row = client.db.fetchone()
        if row is None:
            return cls("en")
        return cls(row['locale'])

    def get_message(self, message_key, **kwargs):
        if self.messages.get(message_key) is None:
            return f"{message_key}"
        message = self.messages.get(message_key)
        for key, value in kwargs.items():
            message = message.replace(f"%{key}%", str(value))
        return message

    #load messages
    def load_messages(self):
        with open(self.locale_file) as f:
            self.messages = json.load(f)