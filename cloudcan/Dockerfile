# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

FROM python:3.10-slim-bookworm

RUN apt-get update && apt-get upgrade -y && apt-get install -y git

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

COPY requirements.txt /requirements.txt
RUN pip install -U pip && pip install -U -r requirements.txt

WORKDIR /app
COPY . /app

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

CMD ["/entrypoint.sh"]

