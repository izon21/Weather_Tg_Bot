import telebot
import requests

# указываем токен для доступа к боту
bot = telebot.TeleBot('You code')

# приветственный текст
start_txt = 'Привет! Тут ты сможешь узнать погоду в своём городе. \nИ  какой лук лучше одеть..'


# обрабатываем старт бота
@bot.message_handler(commands=['start'])
def start(message):
    # выводим приветственное сообщение
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
    w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
    bot.send_message(message.from_user.id, w_now)
    bot.send_message(message.from_user.id, w_feels)
    wind_speed = round(weather_data['wind']['speed'])
    if wind_speed < 5:
        bot.send_message(message.from_user.id, 'Погода хорошая можно одеться как советуют дома моды')
    elif wind_speed < 10:
        bot.send_message(message.from_user.id, 'На улице есть ветер, стоит одеть шапку, как говорит мама.')
    elif wind_speed < 15:
        bot.send_message(message.from_user.id, 'Ветер очень сильный, придется одеть подштанники 😩')
    else:
        bot.send_message(message.from_user.id, 'На улице шторм, в школу лучше не идти')


# запускаем бота
if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e:
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')
