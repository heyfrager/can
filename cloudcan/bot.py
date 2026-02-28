import os
import asyncio
import logging
import pytz
from datetime import datetime
from aiohttp import web
from pyrogram import Client, enums, idle
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, PORT, ADMINS
from plugins.route import web_server
from database.users_db import db
from utils import temp 

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

# ✅ Clean Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="av-botzzx",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
            max_concurrent_transmissions=5,
        )

    async def start(self):
        # ✅ Prevent Double Start
        if self.is_connected:
            return

        await super().start()

        me = await self.get_me()
        temp.ME, temp.U_NAME, temp.B_NAME, temp.B_LINK = me.id, me.username, me.first_name, me.mention
        temp.MAINTENANCE = await db.get_maintenance_mode()
        temp.UPLOAD_MODE = await db.get_upload_mode()

        if temp.MAINTENANCE:
            print("🚨 ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ɪs ᴀᴄᴛɪᴠᴇ")

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🛠  ʟᴏᴀᴅɪɴɢ ᴘʟᴜɢɪɴs...")

        plugin_count = 0
        for root, dirs, files in os.walk("plugins"):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    print(f"🔄 ʟᴏᴀᴅᴇᴅ : {file}")
                    plugin_count += 1
        
        print(f"🎉 ᴛᴏᴛᴀʟ {plugin_count} ᴘʟᴜɢɪɴs ɪᴍᴘᴏʀᴛᴇᴅ !")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        print(f"⚡ {me.first_name} ɪs ɴᴏᴡ ᴏɴʟɪɴᴇ")

        admins = ADMINS if isinstance(ADMINS, list) else [ADMINS] if ADMINS else []

        for admin in admins:
            try:
                await self.send_message(
                    chat_id=admin,
                    text=f"<b>✨ {me.first_name} ɪs ɴᴏᴡ ᴏɴʟɪɴᴇ !</b>",
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                pass

        if LOG_CHANNEL:
            tz = pytz.timezone('Asia/Kolkata')
            now = datetime.now(tz)
            try:
                await self.send_message(
                    LOG_CHANNEL,
                    text=f"<b>🚀 ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ</b>\n"
                         f"➖➖➖➖➖➖➖➖➖➖➖\n"
                         f"<b>📅 ᴅᴀᴛᴇ :</b> <code>{now.strftime('%Y-%m-%d')}</code>\n"
                         f"<b>⏰ ᴛɪᴍᴇ :</b> <code>{now.strftime('%H:%M:%S %p')}</code>\n"
                         f"<b>🌍 ᴛɪᴍᴇᴢᴏɴᴇ :</b> <code>Asia/Kolkata</code>\n"
                         f"➖➖➖➖➖➖➖➖➖➖➖",
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                pass

    async def stop(self, *args):
        if self.is_connected:
            await super().stop()
        print("🛑 ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ")


if __name__ == "__main__":
    
    # ✅ Initialize Bot
    app = Bot()

    async def start_services():
        print(r"""
    ___    _    __      ____        __       
   /   |  | |  / /     / __ )____  / /______ 
  / /| |  | | / /_____/ __  / __ \/ __/ ___/ 
 / ___ |  | |/ /_____/ /_/ / /_/ / /_(__  )  
/_/  |_|  |___/     /_____/\____/\__/____/   

        ᴀᴠ ʙᴏᴛᴢ - ʙᴏᴛ ᴡᴏʀᴋɪɴɢ ᴘʀᴏᴘᴇʀʟʏ 🚀
""")
        # 1. Start Bot
        await app.start()

        # 2. Start Web Server
        app_instance = await web_server(app)
        runner = web.AppRunner(app_instance)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", int(PORT))
        await site.start()

        print(f"🌐 ᴡᴇʙ sᴇʀᴠᴇʀ ʟɪᴠᴇ ᴏɴ ᴘᴏʀᴛ {PORT}")

        # 3. Idle to keep running
        await idle()
        
        # 4. Stop Bot on exit
        await app.stop()

    # ✅ FIXED LOOP LOGIC (Do not create new loop manually)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
    
