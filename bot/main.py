"""
This is a download bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputFile, InputMedia, InlineKeyboardButton, \
    InlineKeyboardMarkup
from pytube import YouTube
from random import randint
import os

from requests_ import request_tiktok


def downloadvideoyoutube(link,itag,type,path):
    try:
        yt = YouTube(link)
        stream = yt.streams.get_by_itag(itag)
        filename = str(randint(100000000, 100000000000))
        if type=='video':
            filename += '.mp4'
        else:
            filename += '.mp3'
        stream.download(output_path=path,filename=filename,timeout=100,max_retries=3)
        return [filename,yt.title]
    except Exception as e:
        print(e)
        return False

downloads = {}


API_TOKEN = '5346182572:AAHc-WGROVX-bzCkF9b2Qw8v9BgABcUVMxE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm DownloaderBot!\nSend me Instagram, Youtube, Tik-Tok video or post link and "
                        "download now!\nPowered "
                        "by: t.me/mal_un ")


@dp.message_handler()
async def main(message: types.Message):
    """
    :param message:
    :return:
    """
    m = await message.answer('Tekshirilmoqda...')
    if "instagram" in message.text:
        await m.edit_text('Instagram post.')

    elif 'you' in message.text:
        await m.edit_text('Youtube video.')
        key = str(randint(1000000, 10000000))
        downloads[key] = message.text
        try:
            yt = YouTube(message.text)
            keyboard = InlineKeyboardMarkup(row_width=2)
            for i in yt.streams:
                if 'acodec' in str(i):
                    i1 = str(i).split(' ')[1:]
                    itag = str(str(i1[0]).split('=')[1])[1:-1]
                    type = str(i1[-1]).split('=')[1][1:-2]
                    res_abr = str(str(i1[2]).split('=')[1])[1:-1]
                    btn_text = f"{type} {res_abr}"
                    btn_callback_data = f"downloadvideo_youtube_{key}_{itag}_{type}"
                    button = InlineKeyboardButton(btn_text, callback_data=btn_callback_data)
                    keyboard.insert(button)
            btns = keyboard
        except Exception as e:
            print(e)
            btns = False
        if btns:
            await m.edit_text('Sifatni tanlang', reply_markup=btns)
        else:
            await message.reply("Yuklab olishni iloji bo'lmadi!")
    elif "likee" in message.text:
        await m.edit_text('Likee video.')

    elif "tiktok" in message.text:
        await m.edit_text('Tik-tok video.')
        await m.edit_text(text=request_tiktok(message.text, m.chat.id))

@dp.callback_query_handler(text_contains='downloadvideo_')
async def menu(call: types.CallbackQuery):
    if call.data and call.data.startswith("downloadvideo_youtube_"):
        await call.message.edit_text('Yuklab olinmoqda...')
        key, itag, type=call.data.split('_')[2:]
        link = downloads[str(key)]
        name = downloadvideoyoutube(link=link, itag=itag, type=type, path=f"videos/youtube/{call.message.chat.id}/")
        await call.message.delete()
        if name:
            video = open(f"videos/youtube/{call.message.chat.id}/" + name[0], 'rb')
            if type=='video':
                try:
                    await call.message.answer_video(video=video,caption=name[1])
                except:
                    await call.message.answer('Vide limitdan oshib ketdi!')
            else:
                try:
                    await call.message.answer_audio(audio=video,caption=name[1])
                except:
                    await call.message.answer('audio limitdan oshib ketdi!')
            video.close()
            os.remove(f"videos/youtube/{call.message.chat.id}/{name[0]}")
        else:
            await call.message.reply("Yuklab olishni iloji bo'lmadi!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)