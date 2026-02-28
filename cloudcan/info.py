from os import environ

def str_to_bool(val):
    return str(val).lower() in {"true", "yes", "1", "t", "y"}

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

API_ID = int(environ.get('API_ID', '80656'))
API_HASH = environ.get('API_HASH', 'd927c13beaaf5110f27c071273')
BOT_TOKEN = environ.get("BOT_TOKEN", "85449448:AAFWldQobm7UhOqH7WPFaSc9bulEWk")
PORT = environ.get("PORT", "8080")
START_PIC = environ.get("START_PIC", "https://o.uguu.se/eKNoswZZ.jpg")

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

ADMINS = list(map(int, environ.get("ADMINS", "5977931010").split()))
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1002110971750"))
DB_URL = environ.get('DATABASE_URI', "mongodb+srv://-TOT:IMGT@cluster0.1rr6x.mongodb.net/?appName=Cluster0")

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

AUTH_CHANNEL = list(map(int, environ.get("AUTH_CHANNEL", "-1002102037760 -1002012150170").split()))
AUTH_REQ_CHANNEL = list(map(int, environ.get("AUTH_REQ_CHANNELS", "-1003615673266").split()))
FSUB = str_to_bool(environ.get("FSUB", "True"))
AUTH_PICS = environ.get("AUTH_PICS", "https://files.catbox.moe/facpku.jpg")
CHANNEL = environ.get("CHANNEL", "https://t.me/AV_BOTz_UPDATE")
SUPPORT = environ.get("SUPPORT", "https://t.me/AV_SUPPORT_GROUP")
APP_URL = environ.get("APP_URL", "https://manual-nikolia-totzvvv-5115e05f.koyeb.app/")

