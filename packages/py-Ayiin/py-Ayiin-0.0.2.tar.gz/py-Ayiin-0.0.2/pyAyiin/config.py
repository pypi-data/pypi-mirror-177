import sys

from decouple import config

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class Var(object):
    # mandatory
    API_ID = (
        int(sys.argv[1]) if len(sys.argv) > 1 else config("API_ID", default=6, cast=int)
    )
    API_HASH = (
        sys.argv[2]
        if len(sys.argv) > 2
        else config("API_HASH", default="eb06d4abfb49dc3eeb1aeb98ae0f581e")
    )
    STRING_1 = config("STRING_1", default=None)
    STRING_2 = config("STRING_2", default=None)
    STRING_3 = config("STRING_3", default=None)
    STRING_4 = config("STRING_4", default=None)
    STRING_5 = config("STRING_5", default=None)
    SESSION_1 = config("SESSION_1", default=None)
    SESSION_2 = config("SESSION_2", default=None)
    SESSION_3 = config("SESSION_3", default=None)
    SESSION_4 = config("SESSION_4", default=None)
    SESSION_5 = config("SESSION_5", default=None)
    REDIS_URI = (
        config("REDIS_URI", default=None) or config("REDIS_URL", default=None)
    )
    REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
    # extras
    BOT_TOKEN = config("BOT_TOKEN", default=None)
    LOG_CHAT = config("LOG_CHAT", default=0, cast=int)
    HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
    HEROKU_API = config("HEROKU_API", default=None)
    TEMP_DOWNLOAD_DIRECTORY = config("TEMP_DOWNLOAD_DIRECTORY", default="./downloads")
    # for railway
    REDISPASSWORD = config("REDISPASSWORD", default=None)
    REDISHOST = config("REDISHOST", default=None)
    REDISPORT = config("REDISPORT", default=None)
    REDISUSER = config("REDISUSER", default=None)
    # for sql
    DATABASE_URL = config("DATABASE_URL", default=None)
    # for MONGODB users
    MONGO_URI = config("MONGO_URI", default=None)
    # for Okteto Platform
    OKTETO = config("OKTETO", cast=bool, default=False)


class CheckString(Var):
    async def check_start(self, pyro=False):
        if not pyro:
            TELETHON_STRING = [string for string in [self.STRING_1, self.STRING_2, self.STRING_3, self.STRING_4, self.STRING_5] if string]
        else:
            PYROGRAM_STRING = [session for session in [self.SESSION_1, self.SESSION_2, self.SESSION_3, self.SESSION_4, self.SESSION_5] if session]
