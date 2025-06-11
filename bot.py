import asyncio
import logging
import sys
from os import getenv
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    ReplyKeyboardRemove,
)


# Токен бота из переменных окружения (.env файла)
TOKEN = getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# ==================== ХЕНДЛЕРЫ КОМАНД ====================
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать! Выберите тип клавиатуры:",
        reply_markup=main_menu_kb()
    )


@dp.message(Command("remove"))
async def cmd_remove(message: Message):
    """Удаляет клавиатуру"""
    await message.answer(
        "Клавиатура удалена",
        reply_markup=ReplyKeyboardRemove()
    )


# ==================== REPLY КНОПКИ ====================
def main_menu_kb() -> ReplyKeyboardMarkup:
    """Главное меню с Reply кнопками"""
    buttons = [
        [KeyboardButton(text="Обычные кнопки")],
        [KeyboardButton(text="Инлайн кнопки")],
        [KeyboardButton(text="Запросить контакт", request_contact=True),
         KeyboardButton(text="Запросить локацию", request_location=True)]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


@dp.message(F.text == "Обычные кнопки")
async def reply_buttons(message: Message):
    await message.answer(
        "Пример обычных кнопок (ReplyKeyboard):",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Кнопка 1"), KeyboardButton(text="Кнопка 2")],
                [KeyboardButton(text="Вернуться в главное меню")]
            ],
            resize_keyboard=True
        )
    )


# ==================== ИНЛАЙН КНОПКИ ====================
def inline_buttons_kb() -> InlineKeyboardMarkup:
    """Клавиатура с inline кнопками"""
    buttons = [
        [InlineKeyboardButton(text="Кнопка с callback", callback_data="btn1")],
        [InlineKeyboardButton(text="Кнопка со ссылкой", url="https://aiogram.dev")],
        [InlineKeyboardButton(text="Веб-приложение", web_app=WebAppInfo(url="https://example.com"))],
        [InlineKeyboardButton(text="Поделиться", switch_inline_query="Проверь этого бота!")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.message(F.text == "Инлайн кнопки")
async def inline_buttons(message: Message):
    await message.answer(
        "Пример inline-кнопок:",
        reply_markup=inline_buttons_kb()
    )


@dp.callback_query(F.data == "btn1")
async def inline_callback(callback: CallbackQuery):
    await callback.answer("Вы нажали inline кнопку!", show_alert=True)


# ==================== СПЕЦИАЛЬНЫЕ КНОПКИ ====================
@dp.message(F.contact)
async def got_contact(message: Message):
    """Обработчик полученного контакта"""
    phone = message.contact.phone_number
    await message.answer(f"Спасибо, ваш телефон {phone} был получен!")


@dp.message(F.location)
async def got_location(message: Message):
    """Обработчик полученной локации"""
    lat = message.location.latitude
    lon = message.location.longitude
    await message.answer(f"Ваши координаты: {lat}, {lon}")


# ==================== ЗАПУСК БОТА ====================
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())