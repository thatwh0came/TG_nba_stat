import telebot
from telebot import types
import sqlite3
import datetime


months = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}

conn = sqlite3.connect('Stat_data_base.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM stats')
rows = cursor.fetchall()

bot = telebot.TeleBot("")
bot.set_webhook()

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
itembtn1 = types.KeyboardButton('Присылать результаты')
menu_keyboard.add(itembtn1)

@bot.message_handler(commands=['start'])
def welcome_message(message):
    username = message.from_user.username
    if username:
        bot.send_message(chat_id=message.chat.id, text = f"Здаров заебал, {username}\nЯ буду присылать тебе результаты матчей Национальной Баскетбольной Ассоциации")
    else:
        bot.send_message(chat_id=message.chat.id, text = f"Здаров, лысый\nЯ буду присылать тебе результаты твоих любимых команд Национальной Баскетбольной Ассоциации")
    bot.send_message(message.chat.id, "Нажми на кнопку, чтобы начать получать рассылку результатов", reply_markup=menu_keyboard)


@bot.message_handler(commands=['data'])
def send_data(message):
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    month_name = months[month]
    date_message = f"{day} {month_name}"
    bot.send_message(message.chat.id, f"⬇️Результаты матчей за {date_message}⬇️")
    for row in rows:
        t1 = row[0]
        t2 = row[3]
        r1 = row[1]
        r2 = row[2]
        tp1 = row[4]
        tp2 = row[5]
        tps1 = row[6]
        tps2 = row[7]
        rec1 = row[8]
        rec2 = row[9]
        # Объединение значений в одну строку
        combined_message = f"""{t1} ({rec1}): {r1}
{t2} ({rec2}): {r2}
⭐️{tp1}: {tps1}
⭐️{tp2}: {tps2}"""
        bot.send_message(message.chat.id, combined_message)


@bot.message_handler(func=lambda message: True)
def handle_callback(message):
    if message.text == 'Присылать результаты':
        bot.send_message(message.chat.id, "Рассылка запущена", reply_markup=types.ReplyKeyboardRemove())


bot.polling()
