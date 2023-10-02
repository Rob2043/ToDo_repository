import telebot
from telebot import types
import random

token = '6557253961:AAGVzm1yrU6hNf_YABjq7EJTmaT1lMwBRTE'

bot = telebot.TeleBot(token)

HELP = """
/help - вывести список доступных команд.
/add - добавить задачу в список (название задачи запрашиваем у пользователя).
/show - напечатать все добавленные задачи.
/random - добавить случайную задачу на дату Сегодня"""

RANDOM_TASKS = ["Записаться на курс в Нетологию", "Написать Гвидо письмо",
                "Покормить кошку", "Помыть машину"]

tasks = {}

day = ""


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton(text='Да', callback_data='yes')
    no_button = types.InlineKeyboardButton(text='Нет', callback_data='no')
    markup.add(yes_button, no_button)

    bot.send_message(
        message.chat.id,
        "Привет! Я твой помощник в домашних делах и не только. Хочешь записать свою задачу?",
        reply_markup=markup
    )


def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = [task]


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=["add"])
def add_day(message):
    bot.send_message(message.chat.id, "Напишите день, на который будете добавлять задачу:")
    bot.register_next_step_handler(message, add_task)


def add_task(message):
    global day
    day = message.text.lower()
    bot.send_message(message.chat.id, "Напишите свою задачу:")
    bot.register_next_step_handler(message, save_task)


def save_task(message):
    task = message.text
    add_todo(day, task)
    text = f"Задача '{task}' добавлена на дату: {day}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["random"])
def random_add(message):
    date = "Сегодня".lower()
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    text = f"Задача '{task}' добавлена на дату: {date}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["show"])
def show(message):
    bot.send_message(message.chat.id, "Напишите день, на который была добавлена задача:")
    bot.register_next_step_handler(message, show_tasks)

def show_tasks(message):
    date = message.text.lower()
    text = ""
    if date in tasks:
        text = date.upper() + "\n"
        for i, task in enumerate(tasks[date], start=1):
            text += f"{i}. {task}\n"
    else:
        text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)

@bot.callback_query_handler(func=lambda call: True)
def answer_start(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_task = types.KeyboardButton('/add')
        item_show = types.KeyboardButton('/show')
        item_random = types.KeyboardButton("/random")
        markup_reply.add(item_task, item_show, item_random)
        bot.send_message(
            call.message.chat.id,
            "Выберите одну из команд:",
            reply_markup=markup_reply
        )
    elif call.data == 'no':
        pass


# Постоянно обращается к серверам Телеграм
bot.polling(none_stop=True)
