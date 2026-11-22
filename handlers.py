from aiogram import Router , F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums import ChatAction
import asyncio
import logging
from datetime import datetime
import html

router = Router()
log = logging.getLogger(__name__)
STICKER_ID = "CAACAgIAAxkBA7bpYGsCGfs6lslpyiTNyXf7oOwEl2fSAAJ0SQACoCf4SntfJDgZ15ogPQQ"
emoji_user = '5256143829672672750'
emoji_thumbnail = '5258477770735885832'
emoji_caption = '5258328383183396223'

def user_block(user) -> str:
    is_bot = "✅" if user.is_bot else "❌"
    is_premium = "✅" if getattr(user, "is_premium", False) else "❌"
    username = (
        f'<a href="https://t.me/{user.username}">@{user.username}</a>'
        if user.username else "—"
    )
    lang = user.language_code or "—"
    return (
        f"<b><tg-emoji emoji-id='{emoji_user}' >👤</tg-emoji> User information</b>\n\n"
        f"<blockquote><b>id : </b><code>{user.id}</code>\n"
        f"<b>name : </b>{html.escape(user.first_name)}\n"
        f"<b>username : </b>{username}\n"
        f"<b>bot : </b>{is_bot}\n"
        f"<b>premium : </b>{is_premium}\n"
        f"<b>language : </b>{lang}</blockquote>\n\n"
    )

def thumb_block(t) -> str:
    return (
        f"\n<b><tg-emoji emoji-id='{emoji_thumbnail}'>📄</tg-emoji> Thumbnail</b>\n"
        f"<blockquote><b>width : </b>{t.width}\n"
        f"<b>height : </b>{t.height}\n"
        f"<b>file_id : </b><code>{t.file_id}</code>\n"
        f"<b>file_unique_id : </b><code>{t.file_unique_id}</code></blockquote>\n"
    )

def caption_block(message: Message) -> str:
    if not message.caption:
        return ""
    return (
        f"\n<b><tg-emoji emoji-id='{emoji_caption}'>📖</tg-emoji> Caption</b>\n"
        f"<blockquote>{html.escape(message.caption)}</blockquote>"
    )
@router.message(CommandStart())
async def cmd_start(message : Message):
    log.info(f"Пользователь {message.from_user.id} (@{message.from_user.username}) запустил бота")
    await message.bot.send_chat_action(
        chat_id = message.chat.id,
        action = ChatAction.TYPING
    )
    await asyncio.sleep(0.3)
    user_id = message.from_user.id
    await message.answer_sticker(STICKER_ID)
    await message.answer(f"""
Привет! 👋 Я бот, который помогает быстро узнать ID в Telegram.

Отправь или перешли мне любое сообщение, контакт, канал или группу — и я сразу пришлю их точный ID. 

Твой личный ID : {user_id}""")


@router.message(Command("info"))
async def cmd_info(message: Message):
    user = message.from_user
    if user is None:
        return

    is_bot = "✅" if user.is_bot else "❌"
    is_premium = "✅" if getattr(user, "is_premium", False) else "❌"
    username = f'<a href="https://t.me/{user.username}">@{user.username}</a>' if user.username else "—"
    lang = user.language_code or "—"

    text = (
        "👤 <b><tg-emoji emoji-id='{emoji_user}' >👤</tg-emoji> User information</b>\n\n"
        f"<blockquote><b>id : </b> <code> {user.id}</code>\n"
        f"<b>name : </b>  {user.first_name}\n"
        f"<b>username : </b>  {username}\n"
        f"<b>bot : </b>  {is_bot}\n"
        f"<b>premium : </b>  {is_premium}\n"
        f"<b>language : </b>  {lang}\n</blockquote>"
    )
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

@router.message(Command("dev"))
async def cmd_owner(message : Message):
    await message.bot.send_chat_action(
            chat_id=message.chat.id, 
            action=ChatAction.TYPING
        )
    await asyncio.sleep(0.3)
    text = (
        "💎<b> Project information.</b>\n\n"
        "<blockquote>👤 <b> Developer:</b> @kiloware\n"
        "📩 <b> Contact:</b> <a href='https://t.me/kiloware'> Send a DM.</a>\n"
        "🐙 <b> GitHub:</b> <a href='https://github.com/l1unyyy'>github.com/l1unyyy</a></blockquote>"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(F.sticker)
async def on_sticker(message : Message):
    user = message.from_user
    s = message.sticker
    if user is None:
            return
    emoji_sticker = '5258179403652801593'
    text = user_block(user) + (
    
        f"<b><tg-emoji emoji-id='{emoji_sticker}' >❤️</tg-emoji> Sticker information</b>\n\n"
        f"<b>width : </b>  {s.width}\n"
        f"<b>height : </b>  {s.height}\n"
        f"<b>emoji : </b>  {s.emoji}\n"
        f"<b>set_name : </b>  {s.set_name}\n"
        f"<b>is_video : </b>  {s.is_video}\n"
        f"<b>type : </b>  {s.type}\n\n"
            
    )
    if s.premium_animation:
         p = s.premium_animation
         emoji_id = '5258185631355378853'
         text += (
        f"<b><tg-emoji emoji-id='{emoji_id}' >⭐</tg-emoji> Premium animation</b>\n\n "
        f"<b>file_id : </b><code>  {p.file_id}</code>\n"
        f"<b>file_unique_id : </b> <code> {p.file_unique_id}</code>\n"
        f"<b>file_size : </b> {p.file_size / 1000:.2f} kB\n"
    )
    text += (
        
        f"<b>file_id : </b> <code> {s.file_id}</code>\n"
        f"<b>file_unique_id : </b><code>  {s.file_unique_id}</code>\n"
        f"<b>file_size : </b> {s.file_size / 1000:.2f} kB \n"
    )
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)
        
        
@router.message(F.photo)
async def on_sticker(message : Message):
    user = message.from_user
    ph = message.photo[-1]

    if user is None:
            return
    is_bot = "✅" if user.is_bot else "❌"
    is_premium = "✅" if getattr(user, "is_premium", False) else "❌"
    username = f'<a href="https://t.me/{user.username}">@{user.username}</a>' if user.username else "—"
    lang = user.language_code or "—"
    emoji_user = '5256143829672672750'
    emoji_photo = '5258205968025525531'
    emoji_caption = '5258328383183396223'
    
    text = (
            f"\n<b><tg-emoji emoji-id='{emoji_user}' >👤</tg-emoji> User information</b>\n\n"
            f"<blockquote><b>id : </b> <code> {user.id}</code>\n"
            f"<b>name : </b>  {user.first_name}\n"
            f"<b>username : </b>  {username}\n"
            f"<b>bot : </b>  {is_bot}\n"
            f"<b>premium : </b>  {is_premium}\n"
            f"<b>language : </b>  {lang}</blockquote>\n\n"

            f"<b><tg-emoji emoji-id='{emoji_photo}'>📸</tg-emoji> Photo information</b>\n\n"
            f"<b>width : </b>  {ph.width}\n"
            f"<b>height : </b>  {ph.height}\n"
            f"<b>file_id : </b> <code> {ph.file_id} </code>\n"
            f"<b>file_unique_id : </b> <code> {ph.file_unique_id}</code>\n"
            f"<b>file size : </b>  {(ph.file_size )/ 1000:.2f} kB\n"
    )
    if message.caption :
        text += f"\n <b><tg-emoji emoji-id='{emoji_caption}' >📖</tg-emoji> Caption</b>\n<blockquote>{message.caption}</blockquote>"
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

@router.message(F.document)
async def on_sticker(message : Message):
    user = message.from_user
    d = message.document

    if user is None:
            return
    
    is_bot = "✅" if user.is_bot else "❌"
    is_premium = "✅" if getattr(user, "is_premium", False) else "❌"
    username = f'<a href="https://t.me/{user.username}">@{user.username}</a>' if user.username else "—"
    lang = user.language_code or "—"
    emoji_user = '5256143829672672750'
    emoji_document = "5258134813302332906"
    emoji_thumbnail = '5258477770735885832'
    emoji_caption = '5258328383183396223'
    text = (
            f"\n<b><tg-emoji emoji-id='{emoji_user}' >👤</tg-emoji> User information</b>\n\n"
            f"<blockquote><b>id : </b> <code> {user.id}</code>\n"
            f"<b>name : </b>  {user.first_name}\n"
            f"<b>username : </b>  {username}\n"
            f"<b>bot : </b>  {is_bot}\n"
            f"<b>premium : </b>  {is_premium}\n"
            f"<b>language : </b>  {lang}</blockquote>\n\n"

            f"\n<b><tg-emoji emoji-id='{emoji_document}'>📦</tg-emoji> Document information</b>\n\n"
            f"<b>file_name : </b> {html.escape(d.file_name or "-")} \n"
            f"<b>mime_type : </b>  {d.mime_type or "-"}\n"
            f"<b>file_id : </b> <code> {d.file_id}</code>\n"
            f"<b>file_unique_id : </b> <code> {d.file_unique_id}</code>\n"
            f"<b>file_size : </b>  {(d.file_size or 0) / 1000:.2f} kB \n"
    )
    if d.thumbnail:
        t  = d.thumbnail
        text += (
            "\n<b><tg-emoji emoji-id='{emoji_thumbnail}'>📄</tg-emoji> Thumbnail</b>\n"
            f"<blockquote><b>width : </b>{t.width}\n"
            f"<b>height : </b>{t.height}\n"
            f"<b>file_id : </b><code>{t.file_id}</code>\n"
            f"<b>file_unique_id : </b><code>{t.file_unique_id}</code>\n"
        )
    if message.caption :
            text += f"\n <b><tg-emoji emoji-id='{emoji_caption}' >📖</tg-emoji> Caption</b>\n<blockquote>{html.escape(message.caption)}</blockquote>"
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)
    
@router.message(F.audio)
async def on_sticker(message : Message):
    user = message.from_user
    a = message.audio

    if user is None:
            return
    
    is_bot = "✅" if user.is_bot else "❌"
    is_premium = "✅" if getattr(user, "is_premium", False) else "❌"
    username = f'<a href="https://t.me/{user.username}">@{user.username}</a>' if user.username else "—"
    lang = user.language_code or "—"
    m,s = divmod(a.duration, 60)
    emoji_user = '5256143829672672750'
    emoji_audio = "5258334469152054985"
    emoji_thumbnail = '5258477770735885832'
    emoji_caption = '5258328383183396223'
    text = (
            f"\n<b><tg-emoji emoji-id='{emoji_user}' >👤</tg-emoji> User information</b>\n\n"
            f"<blockquote><b>id : </b> <code> {user.id}</code>\n"
            f"<b>name : </b>  {user.first_name}\n"
            f"<b>username : </b>  {username}\n"
            f"<b>bot : </b>  {is_bot}\n"
            f"<b>premium : </b>  {is_premium}\n"
            f"<b>language : </b>  {lang}</blockquote>\n\n"

            f"\n<b><tg-emoji emoji-id='{emoji_audio}'>🎶</tg-emoji> Audio information</b>\n\n"
            f"<b>title : </b> {html.escape(a.title or "-")} \n"
            f"<b>performer : </b> {html.escape(a.performer or "-")}\n"
            f"<b>file_name : </b> {html.escape(a.file_name or "-")}\n"
            f"<b>duration : </b> {m}:{s:02d}\n"
            f"<b>mime_type : </b>  {a.mime_type or "-"}\n"
            f"<b>file_id : </b> <code> {a.file_id} </code>\n"
            f"<b>file_unique_id : </b> <code> {a.file__unique_id} </code>\n"
            f"<b>file_size : </b> {(a.file_size or 0) / 1000:.2f} kB\n"
    )
    if a.thumbnail:
        t  = a.thumbnail
        text += (
            "\n<b><tg-emoji emoji-id='{emoji_thumbnail}'>📄</tg-emoji> Thumbnail</b>\n"
            f"<blockquote><b>width : </b>{t.width}\n"
            f"<b>height : </b>{t.height}\n"
            f"<b>file_id : </b><code>{t.file_id}</code>\n"
            f"<b>file_unique_id : </b><code>{t.file_unique_id}</code>\n"
        )
    if message.caption :
            text += f"\n <b><tg-emoji emoji-id='{emoji_caption}' >📖</tg-emoji> Caption</b>\n<blockquote>{html.escape(message.caption)}</blockquote>"
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)
    