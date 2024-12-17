from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, CallbackQuery, Message

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    return message.answer("/dashboard")