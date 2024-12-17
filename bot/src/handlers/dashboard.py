from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, CallbackQuery, Message
from src.utils.formatters import format_datetime
from src.utils.api import TaskManager
from src.core.config import settings
from aiogram.enums import ParseMode


dashboard_router = Router()

@dashboard_router.message(Command("dashboard"))
async def get_dashboard(message: Message):
    task_manager = TaskManager()
    tasks = await task_manager.get_my_tasks()
    
    items = tasks.get("items", [])  # Берем 'items' или пустой список, если его нет

    # Создаем список задач
    task_list = "\n".join([f"{item["message"]} \n Создано: {format_datetime(item["created_at"])} \n Обновлено: {format_datetime(item["updated_at"])}" for item in items])  # Предполагаем, что 'message' - это то, что тебе нужно

    if not task_list:  # Если список пуст
        task_list = "Нет доступных задач!"

    await message.answer(task_list, parse_mode=ParseMode.HTML)

