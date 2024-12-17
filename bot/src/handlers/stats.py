from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, CallbackQuery, Message

stats_router = Router()


@stats_router.message(Command("dashboard"))
async def get_stats(message: Message):
    chat_member_seamusicmgmt = await message.bot.get_chat_member("@seamusicmgmt", message.from_user.id)
    chat_member_fasttube = await message.bot.get_chat_member("@fasttubeofficial", message.from_user.id)

    if chat_member_seamusicmgmt.status in ["member", "administrator", "creator"] and chat_member_fasttube.status in ["member", "administrator", "creator"]:
        caption = f"Привет, {message.from_user.username}! Создано разработчиком @whyspacy как часть проекта @seamusicmgmt. Бот может создавать видео из mp3 и изображения или видео (зацикливая его на всю продолжительность аудио), а затем при желании вы можете выложить видео на ютуб НАПРЯМУЮ из этого телеграм бота.\n\n/start - перезапустить \n/profile - ваш профиль\n/create_with_photo - Создать видео из фото\n/create_with_video - Создать зацикливающееся видео\n/help - все комманды \n\nНа корм разработчику и на хостинг: 2202206254377430 (Сбер)"
        try:
            photo = FSInputFile("src/assets/fasttube-description-picture.png")
        except Exception as e:
            print(e)
        await message.answer_photo(photo=photo, caption=caption, reply_markup=main)
    else:
        await message.answer("Для начала работы бота, нужно подписаться на создателя и канал проекта (там есть еще сервисы для артистов и продюсеров)", reply_markup=check_subscribe)
    