import os
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from info import LOG_CHANNEL, ADMINS, FSUB
from utils import upload_to_catbox, upload_to_uguu
from plugins.fsub import is_user_joined
from database.users_db import db

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

MEDIA_GROUPS = set()

@Client.on_message(filters.photo | filters.animation | filters.video)
async def upload_media(client: Client, message: Message):
 
    if FSUB and not await is_user_joined(client, message):
        return
    
    if await db.is_banned(message.from_user.id):
        return await message.reply(text="<b>🚫 ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ !\n\n👮‍♂️ ᴄᴏɴᴛᴀᴄᴛ : @AV_OWNER_BOT</b>", quote=True, parse_mode=enums.ParseMode.HTML)

    # ✅ GET CURRENT UPLOAD MODE FROM DB
    upload_mode = await db.get_upload_mode()
    
    # ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
    # ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
    # ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
    # sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
    # ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
    # ────────────────────────────────────────

    # ✅ ALBUM HANDLING
    if message.media_group_id:
        if message.media_group_id in MEDIA_GROUPS: return
        MEDIA_GROUPS.add(message.media_group_id)
        
        status_msg = await message.reply_text(text="<b>⏳ ᴘʀᴏᴄᴇssɪɴɢ ᴀʟʙᴜᴍ...</b>", quote=True, parse_mode=enums.ParseMode.HTML)
        
        try:
            files_list = await client.get_media_group(message.chat.id, message.id)
            total_files = len(files_list)
            uploaded_links = []
            
            for index, msg in enumerate(files_list, start=1):
                current_server = upload_mode.upper()
                await status_msg.edit_text(text=f"<b>📤 ᴜᴘʟᴏᴀᴅɪɴɢ {index}/{total_files} ᴛᴏ {current_server}...</b>", parse_mode=enums.ParseMode.HTML)
                
                file_path = await msg.download()
                link = None
                
                if upload_mode == "uguu":
                    link = await upload_to_uguu(file_path)
                    if not link: link = await upload_to_catbox(file_path)
                else:
                    link = await upload_to_catbox(file_path)
                    if not link: link = await upload_to_uguu(file_path)
                
                if link:
                    await db.add_file(message.from_user.id, link)
                    uploaded_links.append(f"<b>📂 ғɪʟᴇ {index} :</b> <code>{link}</code>")
                
                if os.path.exists(file_path): os.remove(file_path)

            if uploaded_links:
                formatted_links = "\n".join(uploaded_links)
                await status_msg.edit_text(text=f"<b>✅ ᴀʟʙᴜᴍ ᴜᴘʟᴏᴀᴅᴇᴅ !</b>\n\n{formatted_links}\n\n<b>⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : ᴀᴠ ʙᴏᴛᴢ</b>", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                
                if LOG_CHANNEL:
                    try:
                        log_text = f"<b>#AlbumUpload</b>\n\n<b>👤 ᴜsᴇʀ :</b> {message.from_user.mention} (<code>{message.from_user.id}</code>)\n<b>📦 ᴛᴏᴛᴀʟ ғɪʟᴇs :</b> {total_files}\n<b>🕒 ᴛɪᴍᴇ :</b> <code>{message.date}</code>"
                        await client.send_message(chat_id=LOG_CHANNEL, text=log_text, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                    except Exception: pass
            else:
                await status_msg.edit_text("<b>❌ ᴀʟʙᴜᴍ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ !</b>")
        except Exception as e:
            await status_msg.edit_text(f"<b>❌ ᴇʀʀᴏʀ :</b> <code>{str(e)}</code>")
        finally:
            MEDIA_GROUPS.discard(message.media_group_id)
        return

    # ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
    # ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
    # ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
    # sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
    # ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
    # ────────────────────────────────────────

    # ✅ SINGLE FILE HANDLING
    status_msg = await message.reply_text(text="<b>⏳ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴍᴇᴅɪᴀ...</b>", quote=True, parse_mode=enums.ParseMode.HTML)
    file_path = None
    try:
        file_path = await message.download()
        current_server = upload_mode.upper()
        
        await status_msg.edit_text(text=f"<b>📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ {current_server}...</b>", parse_mode=enums.ParseMode.HTML)
        
        link = None
        if upload_mode == "uguu":
            link = await upload_to_uguu(file_path)
            if not link:
                await status_msg.edit_text("<b>⚠️ ᴜɢᴜᴜ ғᴀɪʟᴇᴅ, ᴛʀʏɪɴɢ ᴄᴀᴛʙᴏx...</b>")
                link = await upload_to_catbox(file_path)
        else:
            link = await upload_to_catbox(file_path)
            if not link:
                await status_msg.edit_text("<b>⚠️ ᴄᴀᴛʙᴏx ғᴀɪʟᴇᴅ, ᴛʀʏɪɴɢ ᴜɢᴜᴜ...</b>")
                link = await upload_to_uguu(file_path)
        
        if link:
            await db.add_file(message.from_user.id, link)
            await status_msg.edit_text(
                text=f"<b>✅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘʟᴏᴀᴅᴇᴅ !</b>\n\n<b>🔗 ʟɪɴᴋ :</b> <code>{link}</code>\n<b>⚡ ᴅɪʀᴇᴄᴛ :</b> <a href='{link}'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔗 ᴏᴘᴇɴ ʟɪɴᴋ", url=link)]]),
                parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
            )
            
            if LOG_CHANNEL:
                try:
                    log_text = f"<b>#NewUpload</b>\n\n<b>👤 ᴜsᴇʀ :</b> {message.from_user.mention} (<code>{message.from_user.id}</code>)\n<b>🔗 ʟɪɴᴋ :</b> <code>{link}</code>\n<b>🕒 ᴛɪᴍᴇ :</b> <code>{message.date}</code>"
                    await client.send_message(chat_id=LOG_CHANNEL, text=log_text, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                except Exception: pass
        else:
            await status_msg.edit_text(text="<b>❌ ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ !</b>\n\n<b>> sᴇʀᴠᴇʀs ᴀʀᴇ ʙᴜsʏ, ᴛʀʏ ᴀɢᴀɪɴ.</b>", parse_mode=enums.ParseMode.HTML)
            
    except Exception as e:
        await status_msg.edit_text(text=f"<b>❌ ᴇʀʀᴏʀ :</b> <code>{str(e)}</code>", parse_mode=enums.ParseMode.HTML)
    finally:
        if file_path and os.path.exists(file_path): os.remove(file_path)
    
