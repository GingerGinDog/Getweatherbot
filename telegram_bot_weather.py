import requests
import datetime
from confing import token_bot, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=token_bot)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я скину тебе сводку погоды')

@dp.message_handler()
async def  get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
        }


    try :
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
        data = r.json()


        city = data['name']
        cur_weather  = data['main']['temp']
        temp_max = data['main']['temp_max']
        humidity  = data['main']['humidity']
        wind_s = data['wind']['speed']
        sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        lengt_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        weather_pic = data['weather'][0]['main']
        if weather_pic in code_to_smile:
            wd = code_to_smile[weather_pic]
        else:
            print('Глянь в окно и узнай')

        await message.reply(f"Погода в городе: {city}\nCредняя температура: {cur_weather}\nМаксимальная температура: {temp_max}\n"
              f"Влажность: {humidity}\nСкорость ветра: {wind_s}\nКартинка за окном: {wd}\n"
              f"Время рассвета: {sunrise_time}\nВремя заката: {sunset_time}\nПродолжительность дня: {lengt_of_the_day}\n")

    except:
        await message.reply('\U00002620 Проверьте название города! \U00002620')



if __name__ == '__main__':
    executor.start_polling(dp)