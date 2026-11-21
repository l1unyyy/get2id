from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums import ChatAction
import asyncio
import logging
from datetime import datetime


router = Router()
log = logging.getLogger(__name__)
STICKER_ID = "CAACAgIAAxkBA7bpYGsCGfs6lslpyiTNyXf7oOwEl2fSAAJ0SQACoCf4SntfJDgZ15ogPQQ"

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
        "👤 <b> User information</b>\n\n"
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


