import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import LabeledPrice, Message
from aiogram.types import PreCheckoutQuery
from aiogram.types import ContentType
import yt_dlp
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

print('\n\n https://github.com/Shia2009/ \n\n')



bot = Bot(token='7783596711:AAEdH8ixw4ErNJWiRBbWHNVcjtcxajaIKh0')
admin=''#Укажите id свой кому отпралвять о том что кто то скачивает или удаляет
start_message='Привет ! <b> Отправь мне ссылку на видео которое нужно скачать</b>'#стартовое сообщение
dp = Dispatcher()


class Form(StatesGroup):
    waiting_for_message = State()

# Логирование, которое предоставляет сообщения о статусе бота
logging.basicConfig(level=logging.INFO)



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(start_message, parse_mode='HTML')


def payment_keyboard():
    builder=InlineKeyboardBuilder()
    builder.button(text=f'Оплатить 1 ⭐', pay=True)

    return builder.as_markup()

@dp.message(F.text)#обрабатываем ЛЮБОЕ сообщение
async def with_puree(message: types.Message):
    if message.text=='отправить 1 звезду автору':
        prices = [LabeledPrice(label='XTR', amount=1)]
        await message.answer_invoice(
            title='Поддержка',
            description='Поддержать одной звездой',
            prices=prices,
            provider_token="",
            payload="channel_support",
            currency="XTR",
            reply_markup=payment_keyboard(),
        )
    if message.text.startswith(("https", "http")):
        user_channel_status = await bot.get_chat_member(chat_id='-1002022328830', user_id=message.chat.id)
        if user_channel_status.status != 'left':
            try:
                url = message.text
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': f'{message.chat.id}.%(ext)s',  # шаблон имени файла
                }
            except:
                await bot.send_message(message.from_user.id, '<b>Ошибка в ссылке видео</b>', parse_mode='HTML')
            await bot.send_message(message.from_user.id, '<b>Начинаем скачивать видео...</b>', parse_mode='HTML')
            await bot.send_message(message.from_user.id, '⌛')
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except:
                await bot.send_message(message.from_user.id, '<b>Ошибка в скачивании видео</b>', parse_mode='HTML')
            await bot.send_message(admin, f'Видео скаченно {message.text} @{message.chat.username}')
            await bot.send_message(message.from_user.id, '<b>Отправляем видео...</b>', parse_mode='HTML')
            await bot.send_message(message.from_user.id, '✈')
            video = FSInputFile(fr'{os.getcwd()}\{message.chat.id}.mp4')

            await message.answer_video(
                video=video,
                caption="Ваше видео",
                supports_streaming=True
            )
            os.remove(fr'{os.getcwd()}\{message.chat.id}.mp4')
            kb = [
                [types.KeyboardButton(text="отправить 1 звезду автору")]]
            markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Категория ?")
            await bot.send_message(message.from_user.id, '<b>Поддержать автора 1 звездой</b>', reply_markup=markup, parse_mode='HTML')
            await bot.send_message(admin, f'Видео удаленно {message.text} @{message.chat.username}')
        else:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Подпишитесь на канал!", url="https://t.me/NOMEROK_CHANNEL")],
                [InlineKeyboardButton(text="Проверить еще раз🔄", callback_data="check")]
            ])
            await bot.send_message(message.from_user.id, '❌<b>Вы не подписанны на канал !</b>', reply_markup=kb, parse_mode='HTML')




@dp.callback_query(lambda c: c.data == "check")
async def handle_yes(callback: types.CallbackQuery):
    await callback.answer('Проверка')
    user_channel_status = await bot.get_chat_member(chat_id='-1002022328830', user_id=callback.message.chat.id)
    if user_channel_status.status != 'left':
        await bot.send_message(callback.message.chat.id,'<b>Отправьте ссылку на видео!</b>', parse_mode='HTML')
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Подпишитесь на канал!", url="https://t.me/NOMEROK_CHANNEL")],
            [InlineKeyboardButton(text="Проверить еще раз🔄", callback_data="check")]
        ])
        await bot.send_message(callback.message.chat.id, '<b>Вы не подписаны</b>', reply_markup=kb, parse_mode='HTML')

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@dp.message(F.succesful_payment)
async def process_successful_payment(message: types.Message)->None:
    await message.answer(f'{message.successful_payment.telegram_payment_charge_id}', message_effect_id='5104841245755180586')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())