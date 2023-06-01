
from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
API_ID = int(getenv("API_ID") or 0)
SESSION = getenv("SESSION", "")
OPENAI_API = getenv("OPENAI_API", "")
API_HASH = getenv("API_HASH")
USERBOT_PREFIX = getenv("USERBOT_PREFIX", ".")
PHONE_NUMBER = getenv("PHONE_NUMBER")
SUDO_USERS_ID = list(map(int, getenv("SUDO_USERS_ID", "").split()))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID") or 0)
GBAN_LOG_GROUP_ID = int(getenv("GBAN_LOG_GROUP_ID") or 0)
MESSAGE_DUMP_CHAT = int(getenv("MESSAGE_DUMP_CHAT") or 0)
WELCOME_DELAY_KICK_SEC = int(getenv("WELCOME_DELAY_KICK_SEC", "600"))
MONGO_URL = getenv("MONGO_URL")
ARQ_API_KEY = getenv("ARQ_API_KEY")
ARQ_API_URL = getenv("ARQ_API_URL", "https://arq.hamker.in")
LOG_MENTIONS = getenv("LOG_MENTIONS", "True").lower() in ["true", "1"]
RSS_DELAY = int(getenv("RSS_DELAY", "300"))
PM_PERMIT = getenv("PM_PERMIT", "True").lower() in ["true", "1"]
