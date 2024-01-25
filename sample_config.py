import os

from dotenv import load_dotenv

load_dotenv(
    "config.env" if os.path.isfile("config.env") else "sample_config.env"
)

BOT_TOKEN = os.environ.get("6844364733:AAF0N22YvmmZOE2YXmeBTtBTFniQLPTn_QY")
API_ID = int(os.environ.get("24204113"))
SESSION_STRING = os.environ.get("SESSION_STRING", "")
API_HASH = os.environ.get("d4fad5275d1969ee0e33c92efada3da8")
USERBOT_PREFIX = os.environ.get("USERBOT_PREFIX", ".")
PHONE_NUMBER = os.environ.get("+917377286823")
SUDO_USERS_ID = list(map(int, os.environ.get("5449746093", "").split()))
LOG_GROUP_ID = int(os.environ.get("-4177413357"))
GBAN_LOG_GROUP_ID = int(os.environ.get("-4177413357"))
MESSAGE_DUMP_CHAT = int(os.environ.get("-4177413357"))
WELCOME_DELAY_KICK_SEC = int(os.environ.get("WELCOME_DELAY_KICK_SEC", 600))
MONGO_URL = os.environ.get("mongodb+srv://pranav999:Billy@982@cluster0.0mjgkud.mongodb.net/?retryWrites=true&w=majority")
ARQ_API_KEY = os.environ.get("ARQ_API_KEY")
ARQ_API_URL = os.environ.get("ARQ_API_URL", "https://arq.hamker.dev")
LOG_MENTIONS = os.environ.get("LOG_MENTIONS", "True").lower() in ["true", "1"]
RSS_DELAY = int(os.environ.get("RSS_DELAY", 300))
PM_PERMIT = os.environ.get("PM_PERMIT", "True").lower() in ["true", "1"]
