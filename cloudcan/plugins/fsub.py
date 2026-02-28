import asyncio
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from database.users_db import db
from info import ADMINS, AUTH_CHANNEL, AUTH_REQ_CHANNEL, AUTH_PICS
from utils import temp
from Script import script

logger = logging.getLogger(__name__)

def is_auth_req_channel(_, __, update):
    if not AUTH_REQ_CHANNEL:
        return False
    return update.chat.id in AUTH_REQ_CHANNEL

@Client.on_chat_join_request(filters.create(is_auth_req_channel))
async def join_reqs(client, message: ChatJoinRequest):
    try:
        await db.add_join_req(message.from_user.id, message.chat.id)
    except Exception as e:
        logger.error(f"Error saving join request: {e}")

async def is_req_subscribed(bot, user_id, rqfsub_channels, db):
    btn = []
    for ch_id in rqfsub_channels:
        if await db.has_joined_channel(user_id, ch_id):
            continue
        try:
            member = await bot.get_chat_member(ch_id, user_id)
            if member.status != enums.ChatMemberStatus.BANNED:
                await db.add_join_req(user_id, ch_id)
                continue
        except UserNotParticipant:
            pass 
        except Exception as e:
            logger.error(f"Error checking membership in {ch_id}: {e}")
        
        try:
            chat = await bot.get_chat(ch_id)
            invite = await bot.create_chat_invite_link(
                ch_id,
                creates_join_request=True
            )
            btn.append([InlineKeyboardButton(f"⛔️ ᴊᴏɪɴ {chat.title}", url=invite.invite_link)])
        except ChatAdminRequired:
            logger.warning(f"Bot not admin in {ch_id}")
        except Exception as e:
            logger.warning(f"Invite link error for {ch_id}: {e}")
            
    return btn

async def is_subscribed(bot, user_id, fsub_channels):
    btn = []

    async def check_channel(channel_id):
        try:
            await bot.get_chat_member(channel_id, user_id)
        except UserNotParticipant:
            try:
                chat = await bot.get_chat(int(channel_id))
                invite_link = await bot.create_chat_invite_link(channel_id)
                return InlineKeyboardButton(f"📢 ᴊᴏɪɴ {chat.title}", url=invite_link.invite_link)
            except Exception as e:
                logger.warning(f"Failed to create invite for {channel_id}: {e}")
        except Exception as e:
            logger.exception(f"is_subscribed error for {channel_id}: {e}")
        return None

    tasks = [check_channel(channel_id) for channel_id in fsub_channels]
    results = await asyncio.gather(*tasks)
    for button in results:
        if button:
            btn.append([button])
            
    return btn

async def is_user_joined(client, message):
    user_id = message.from_user.id
    btn = []
    
    if AUTH_CHANNEL:
        btn += await is_subscribed(client, user_id, AUTH_CHANNEL)
    
    if AUTH_REQ_CHANNEL:
        btn += await is_req_subscribed(client, user_id, AUTH_REQ_CHANNEL, db)
    
    if btn:
        btn.append([InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", url=f"https://t.me/{temp.U_NAME}?start=start")])
        reply_markup = InlineKeyboardMarkup(btn)
        
        if AUTH_PICS:
            await message.reply_photo(
                photo=AUTH_PICS,
                caption=script.AUTH_TXT.format(message.from_user.mention),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply_text(
                text=script.AUTH_TXT.format(message.from_user.mention),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        return False
    return True
