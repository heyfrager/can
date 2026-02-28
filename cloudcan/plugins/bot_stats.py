import shutil
import os
from pyrogram import Client, filters, enums
from database.users_db import db
from info import ADMINS

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

@Client.on_message(filters.command('stats') & filters.user(ADMINS) & filters.incoming)
async def get_stats(bot, message):
    status_msg = await message.reply_text("<b>⚡ ꜰᴇᴛᴄʜɪɴɢ sᴛᴀᴛs...</b>", quote=True)
    total_users = await db.total_users_count()
    total_files = await db.total_files_count()
    total_banned = await db.total_banned_users_count() 
    total_join_reqs = await db.req.count_documents({})
    total_web = await db.total_web_uploads_count()
    total, used, free = shutil.disk_usage(".")
    
    # ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
    # ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
    # ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
    # sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
    # ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
    # ────────────────────────────────────────

    stats_message = (
        "<b>📊 ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs</b>\n"
        "➖➖➖➖➖➖➖➖➖➖➖\n"
        f"<b>👤 ᴛᴏᴛᴀʟ ᴜsᴇʀs :</b> <code>{total_users}</code>\n"
        f"<b>🚫 ʙᴀɴɴᴇᴅ ᴜsᴇʀs :</b> <code>{total_banned}</code>\n"
        f"<b>📂 ᴛᴏᴛᴀʟ ғɪʟᴇs :</b> <code>{total_files}</code>\n"
        f"<b>🌐 ᴡᴇʙ ᴜᴘʟᴏᴀᴅs :</b> <code>{total_web}</code>\n"
        f"<b>💡 ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛs :</b> <code>{total_join_reqs}</code>\n"
        "➖➖➖➖➖➖➖➖➖➖➖\n"
        f"<b>💿 ᴛᴏᴛᴀʟ sᴘᴀᴄᴇ :</b> <code>{total / (2**30):.2f} GB</code>\n"
        f"<b>🟢 ғʀᴇᴇ sᴘᴀᴄᴇ :</b> <code>{free / (2**30):.2f} GB</code>\n"
        "➖➖➖➖➖➖➖➖➖➖➖"
    )
    await status_msg.edit(stats_message, parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.del_join_req()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")
    
@Client.on_message(filters.command(["top", "leaderboard", "topusers"]) & filters.user(ADMINS))
async def top_uploaders_handler(client, message):
    status_msg = await message.reply_text("<b>⚡ ᴄᴀʟᴄᴜʟᴀᴛɪɴɢ ᴛᴏᴘ ᴜᴘʟᴏᴀᴅᴇʀs...</b>")
    top_data = await db.get_top_uploaders()
    if not top_data: return await status_msg.edit("<b>❌ ɴᴏ ᴜᴘʟᴏᴀᴅs ғᴏᴜɴᴅ !</b>")

    # ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
    # ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
    # ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
    # sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
    # ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
    # ────────────────────────────────────────

    formatted_list = []
    for index, data in enumerate(top_data, start=1):
        name = await db.get_user_name(data["_id"])
        formatted_list.append(f"{index}. {name} (ID: {data['_id']}) - {data['count']} Files")
    
    total_users = len(top_data)
    if total_users <= 10:
        await status_msg.edit(f"<b>🏆 ᴛᴏᴘ ᴜᴘʟᴏᴀᴅᴇʀs ({total_users}) :</b>\n\n" + "\n".join(formatted_list), parse_mode=enums.ParseMode.HTML)
    else:
        file_path = "Top_Uploaders.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"🏆 TOP UPLOADERS LEADERBOARD\nTotal Active Uploaders: {total_users}\n========================================\n\n" + "\n".join(formatted_list))
        
        # ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
        # ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
        # ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
        # sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
        # ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
        # ────────────────────────────────────────

        await message.reply_document(
            document=file_path,
            caption=f"<b>🏆 ᴛᴏᴘ ᴜᴘʟᴏᴀᴅᴇʀs ʟɪsᴛ</b>\n\n<b>👥 ᴛᴏᴛᴀʟ ᴜsᴇʀs :</b> <code>{total_users}</code>\n<b>📂 ʟɪsᴛ ɪs ʟᴏɴɢ, sᴇɴᴅɪɴɢ ғɪʟᴇ...</b>",
            parse_mode=enums.ParseMode.HTML
        )
        await status_msg.delete()
        if os.path.exists(file_path): os.remove(file_path)
            
