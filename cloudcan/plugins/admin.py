import os
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from database.users_db import db
from info import ADMINS
from utils import temp

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

@Client.on_message(filters.command(["check", "info", "user"]) & filters.user(ADMINS))
async def check_user_details(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try: user_id = int(message.command[1])
        except ValueError: return await message.reply_text("<b>❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ !</b>")
    else:
        return await message.reply_text("<b>⚠️ ɢɪᴠᴇ ᴍᴇ ᴀ ᴜsᴇʀ ɪᴅ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ !\n\nᴇxᴀᴍᴘʟᴇ :</b> <code>/check 12345678</code>", quote=True)
    
    msg = await message.reply_text("<b>⚡ ᴄʜᴇᴄᴋɪɴɢ ᴅᴀᴛᴀʙᴀsᴇ...</b>")
    try:
        user = await client.get_users(user_id)
        name, username, dc_id = user.first_name, f"@{user.username}" if user.username else "None", user.dc_id if user.dc_id else "Unknown"
    except Exception:
        name, username, dc_id = "Unknown User", "None", "Unknown"
    
    db_exist = await db.is_user_exist(user_id)
    total_files = await db.total_files_by_user(user_id)
    exist_text = "✅ ʏᴇs" if db_exist else "❌ ɴᴏ"
    
    text = (
        f"<b>👤 ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>\n➖➖➖➖➖➖➖➖➖➖➖\n"
        f"<b>🆔 ᴜsᴇʀ ɪᴅ :</b> <code>{user_id}</code>\n<b>👤 ɴᴀᴍᴇ :</b> {name}\n"
        f"<b>🔗 ᴜsᴇʀɴᴀᴍᴇ :</b> {username}\n<b>🌐 ᴅᴄ ɪᴅ :</b> {dc_id}\n"
        f"➖➖➖➖➖➖➖➖➖➖➖\n<b>📂 ᴛᴏᴛᴀʟ ᴜᴘʟᴏᴀᴅs :</b> <code>{total_files}</code>\n"
        f"<b>💾 ɪɴ ᴅᴀᴛᴀʙᴀsᴇ :</b> {exist_text}\n➖➖➖➖➖➖➖➖➖➖➖"
    )
    buttons = [[InlineKeyboardButton("🔗 ᴘʀᴏғɪʟᴇ", url=f"tg://user?id={user_id}"), InlineKeyboardButton("🗑️ ᴡɪᴘᴇ ᴅᴀᴛᴀ", callback_data=f"wipe_{user_id}")], [InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close_data")]]
    await msg.edit_text(text=text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=enums.ParseMode.HTML)

@Client.on_callback_query(filters.regex(r"^wipe_"))
async def wipe_user_data_callback(client, query: CallbackQuery):
    if query.from_user.id not in ADMINS: return await query.answer("❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ !", show_alert=True)
    target_id = int(query.data.split("_")[1])
    await query.message.edit_text(
        text=f"<b>⚠️ ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ?</b>\n\nʏᴏᴜ ᴀʀᴇ ᴀʙᴏᴜᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ <b>ᴀʟʟ ғɪʟᴇs</b> ᴏғ ᴜsᴇʀ <code>{target_id}</code>.\nᴛʜɪs ᴄᴀɴɴᴏᴛ ʙᴇ ᴜɴᴅᴏɴᴇ.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ ʏᴇs, ᴅᴇʟᴇᴛᴇ", callback_data=f"confirmwipe_{target_id}"), InlineKeyboardButton("❌ ɴᴏ", callback_data="close_data")]]),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex(r"^confirmwipe_"))
async def confirm_wipe_callback(client, query: CallbackQuery):
    target_id = int(query.data.split("_")[1])
    await db.delete_all_files(target_id)
    await query.message.edit_text(text=f"<b>✅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴡɪᴘᴇᴅ ᴅᴀᴛᴀ ғᴏʀ {target_id} !</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close_data")]]), parse_mode=enums.ParseMode.HTML)

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

@Client.on_message(filters.command("ban") & filters.user(ADMINS))
async def ban_user(client, message):
    if len(message.command) < 2: return await message.reply("<b>⚠️ ɢɪᴠᴇ ᴍᴇ ᴀ ᴜsᴇʀ ɪᴅ ᴛᴏ ʙᴀɴ !</b>")
    try:
        user_id = int(message.command[1])
        await db.add_ban(user_id)
        
        # ✅ Send Notification to User
        try:
            await client.send_message(
                chat_id=user_id,
                text="<b>🚫 ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ !\n\n👮‍♂️ ᴄᴏɴᴛᴀᴄᴛ : @AV_OWNER_BOT</b>",
                parse_mode=enums.ParseMode.HTML
            )
        except Exception: pass
        
        await message.reply(f"<b>🚫 ᴜsᴇʀ {user_id} ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ !</b>")
    except Exception as e: await message.reply(f"❌ ᴇʀʀᴏʀ: {e}")

@Client.on_message(filters.command("unban") & filters.user(ADMINS))
async def unban_user(client, message):
    if len(message.command) < 2: return await message.reply("<b>⚠️ ɢɪᴠᴇ ᴍᴇ ᴀ ᴜsᴇʀ ɪᴅ ᴛᴏ ᴜɴʙᴀɴ !</b>")
    try:
        user_id = int(message.command[1])
        await db.remove_ban(user_id)
        
        # ✅ Send Notification to User
        try:
            await client.send_message(
                chat_id=user_id,
                text="<b>✅ ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ !\n\n😃 ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ɴᴏᴡ.</b>",
                parse_mode=enums.ParseMode.HTML
            )
        except Exception: pass
        
        await message.reply(f"<b>✅ ᴜsᴇʀ {user_id} ʜᴀs ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ !</b>")
    except Exception as e: await message.reply(f"❌ ᴇʀʀᴏʀ: {e}")

@Client.on_message(filters.command(["banned", "banlist"]) & filters.user(ADMINS))
async def banned_users_list(client, message):
    msg = await message.reply_text("<b>⚡ ғᴇᴛᴄʜɪɴɢ ʙᴀɴɴᴇᴅ ᴜsᴇʀs...</b>")
    banned_cursor = await db.get_banned_users()
    banned_list = await banned_cursor.to_list(length=None)
    if not banned_list: return await msg.edit("<b>✅ ɴᴏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs ғᴏᴜɴᴅ !</b>")
    total_banned = len(banned_list)
    
    if total_banned < 10:
        text = f"<b>🚫 ʙᴀɴɴᴇᴅ ᴜsᴇʀs ʟɪsᴛ ({total_banned}) :</b>\n\n"
        for user in banned_list: text += f"👤 <b>{user.get('name', 'Unknown')}</b> (<code>{user['id']}</code>)\n"
        await msg.edit(text, parse_mode=enums.ParseMode.HTML)
    else:
        file_path = "Banned_Users.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"🚫 TOTAL BANNED USERS: {total_banned}\n========================================\n\n")
            for user in banned_list: f.write(f"ID: {user['id']} | Name: {user.get('name', 'Unknown')}\n")
        await message.reply_document(document=file_path, caption=f"<b>🚫 ᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ ᴜsᴇʀs :</b> <code>{total_banned}</code>\n<b>📂 ʟɪsᴛ ɪs ᴛᴏᴏ ʟᴏɴɢ, sᴇɴᴅɪɴɢ ғɪʟᴇ...</b>", parse_mode=enums.ParseMode.HTML)
        await msg.delete()
        if os.path.exists(file_path): os.remove(file_path)

# ── ᴀᴠ ʙᴏᴛᴢ ─────────────────────────────
# ᴜᴘᴅᴀᴛᴇs  : https://t.me/AV_BOTz_UPDATE
# ᴏᴡɴᴇʀ    : @AV_OWNER_BOT
# sᴜᴘᴘᴏʀᴛ  : https://t.me/AV_SUPPORT_GROUP
# ᴄʀᴇᴅɪᴛ   : ᴀᴠ ʙᴏᴛᴢ | ᴀᴍᴀɴ ᴠɪsʜᴡᴀᴋᴀʀᴍᴀ
# ────────────────────────────────────────

@Client.on_message(filters.command("mode") & filters.user(ADMINS))
async def show_upload_mode(client, message):
    current_mode = await db.get_upload_mode()
    
    c_cat = "✅" if current_mode == "catbox" else ""
    c_ugu = "✅" if current_mode == "uguu" else ""
    
    buttons = [
        [InlineKeyboardButton(f"{c_cat} ᴄᴀᴛʙᴏx", callback_data="set_mode_catbox"), InlineKeyboardButton(f"{c_ugu} ᴜɢᴜᴜ", callback_data="set_mode_uguu")],
        [InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close_data")]
    ]
    
    await message.reply_text(
        text=f"<b>⚙️ ᴄᴜʀʀᴇɴᴛ ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ :</b> <code>{current_mode.upper()}</code>\n\n<i>👇 ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴄʜᴀɴɢᴇ sᴇʀᴠᴇʀ.</i>",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True, parse_mode=enums.ParseMode.HTML
    )

@Client.on_callback_query(filters.regex(r"^set_mode_"))
async def set_mode_callback(client, query: CallbackQuery):
    if query.from_user.id not in ADMINS: return await query.answer("❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ !", show_alert=True)
    target_mode = query.data.split("_")[2]
    await db.set_upload_mode(target_mode)
    temp.UPLOAD_MODE = target_mode
    c_cat = "✅" if target_mode == "catbox" else ""
    c_ugu = "✅" if target_mode == "uguu" else ""
    
    buttons = [
        [InlineKeyboardButton(f"{c_cat} ᴄᴀᴛʙᴏx", callback_data="set_mode_catbox"), InlineKeyboardButton(f"{c_ugu} ᴜɢᴜᴜ", callback_data="set_mode_uguu")],
        [InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close_data")]
    ]
    
    await query.message.edit_text(
        text=f"<b>⚙️ ᴄᴜʀʀᴇɴᴛ ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ :</b> <code>{target_mode.upper()}</code>\n\n<i>👇 ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴄʜᴀɴɢᴇ sᴇʀᴠᴇʀ.</i>",
        reply_markup=InlineKeyboardMarkup(buttons), parse_mode=enums.ParseMode.HTML
    )
    await query.answer(f"✅ Mode Changed to {target_mode.upper()}")
    
    
