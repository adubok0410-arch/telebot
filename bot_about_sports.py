import telebot
from telebot import types

bot = telebot.TeleBot('8607180210:AAFxmRkpzj_cF_5hlEptkifqdTagqASa0ac')

user_data = {}
user_state = {}

ACTIVITY = {
    "🟢 Минимальная (сидячая работа)": 1.2,
    "🟡 Низкая (спорт 1-3 дня)": 1.375,
    "🟠 Средняя (спорт 3-5 дней)": 1.55,
    "🔴 Высокая (спорт 6-7 дней)": 1.725,
    "⚡ Очень высокая (физ.работа + спорт)": 1.9
}

GOALS = {
    "🔥 Похудение": 0.85,
    "💪 Набор массы": 1.1,
    "⚖️ Поддержание веса": 1.0
}


def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton('🧮 КАЛЬКУЛЯТОР КБЖУ')
    button2 = types.KeyboardButton("📚 ГАЙДЫ ПО ТРЕНИРОВКАМ")
    button3 = types.KeyboardButton('🏋️ УПРАЖНЕНИЯ')
    button4 = types.KeyboardButton("🔨 РАЗРУШИТЕЛИ МИФОВ")
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)
    return markup


def get_guides_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('ГАЙД(Тренировки)')
    button2 = types.KeyboardButton('ГАЙД(Сушка)')
    button3 = types.KeyboardButton('ГАЙД(Масса)')
    button4 = types.KeyboardButton('🔙 Вернуться в меню')
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)
    return markup


def get_exercises_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('💪 Руки')
    button2 = types.KeyboardButton('🦵 Ноги')
    button3 = types.KeyboardButton('🏋️ Грудь')
    button4 = types.KeyboardButton('🧗 Спина')
    button5 = types.KeyboardButton('🔙 Вернуться в меню')
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)
    markup.row(button5)
    return markup


def get_gender_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(types.KeyboardButton('♂️ Мужской'), types.KeyboardButton('♀️ Женский'))
    return markup


def get_activity_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard = list(ACTIVITY.keys())
    markup.row(types.KeyboardButton(keyboard[0]), types.KeyboardButton(keyboard[1]), types.KeyboardButton(keyboard[2]))
    markup.row(types.KeyboardButton(keyboard[3]), types.KeyboardButton(keyboard[4]))
    return markup


def get_goals_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard = list(GOALS.keys())
    markup.row(types.KeyboardButton(keyboard[0]), types.KeyboardButton(keyboard[1]))
    markup.row(types.KeyboardButton(keyboard[-1]))
    return markup


def remove_keyboard():
    return types.ReplyKeyboardRemove()


def calculate(data):
    age = data['age']
    gender = data['gender']
    height = data['height']
    weight = data['weight']
    basic_metabolism = 0

    if gender == '♂️ Мужской':
        basic_metabolism = (10 * weight) + (6.25 * height) - (5 * age) + 161
    elif gender == '♀️ Женский':
        basic_metabolism = (10 * weight) + (6.25 * height) - (5 * age) - 5

    activity_coefficient = ACTIVITY[data['activity']]
    goal_coefficient = GOALS[data['goal']]

    calories = round(basic_metabolism * activity_coefficient * goal_coefficient)
    proteins = round(calories * 0.3 / 4)
    fats = round(calories * 0.25 / 9)
    carbohydrates = round(calories * 0.45 / 4)

    return {
        'calories': calories,
        'proteins': proteins,
        'fats': fats,
        'carbohydrates': carbohydrates
    }


def format_result(data, result):
    return f"""
🏆 **Твоя норма КБЖУ на день**

🎯 Цель: {data['goal']}
📊 Уровень активности: {data['activity']}

━━━━━━━━━━━━━━━━━
🔥 **Калории:** {result['calories']} ккал
━━━━━━━━━━━━━━━━━

🥩 **Белки:** {result['proteins']} г
🧀 **Жиры:** {result['fats']} г
🍚 **Углеводы:** {result['carbohydrates']} г
    """


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id in user_state:
        del user_state[chat_id]
    if chat_id in user_data:
        del user_data[chat_id]

    welcome_text = """
🏠 **ГЛАВНОЕ МЕНЮ**

Приветствую! 👋

Ты находишься в **главном меню** — здесь собрано всё, что я умею.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *Выбирай нужное из кнопок внизу*

👇👇👇

    """
    bot.send_message(chat_id, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())


@bot.message_handler(func=lambda message: message.text == '🧮 КАЛЬКУЛЯТОР КБЖУ')
def start_calculator(message):
    chat_id = message.chat.id

    user_data[chat_id] = {}
    user_state[chat_id] = "waiting_age"

    bot.send_message(
        chat_id,
        "📊 **КАЛЬКУЛЯТОР КБЖУ**\n\n"
        "Я рассчитаю твою личную норму за 2 минуты.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔢 **Сколько тебе лет?**\n\n(напиши числом)",
        parse_mode="Markdown",
        reply_markup=remove_keyboard()
    )


@bot.message_handler(func=lambda message: message.text == "📚 ГАЙДЫ ПО ТРЕНИРОВКАМ")
def guide_choice(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, '👇 Выбери из кнопок снизу, какой гайд ты хочешь', reply_markup=get_guides_keyboard())


@bot.message_handler(func=lambda message: message.text == "🔨 РАЗРУШИТЕЛИ МИФОВ")
def myths_destroyer_handler(message):
    chat_id = message.chat.id
    with open('Разрушители мифов.pdf', 'rb') as pdf:
        bot.send_document(chat_id, pdf, caption='Разрушители мифов', reply_markup=get_main_keyboard())


@bot.message_handler(func=lambda message: message.text == '🏋️ УПРАЖНЕНИЯ')
def exercises_handler(message):
    chat_id = message.chat.id
    text = """
    🏋️ **БИБЛИОТЕКА УПРАЖНЕНИЙ**

    *Здесь собраны лучшие движения для каждой группы мышц*

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Выбери, что будем качать:

    💪 **РУКИ**
    🦵 **НОГИ**
    🏋️ **ГРУДЬ**
    🧗 **СПИНА**

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    👇 **Нажми на нужную кнопку ниже**
        """
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=get_exercises_keyboard())


@bot.message_handler(func=lambda message: True)
def main(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)

    if chat_id not in user_data:
        user_data[chat_id] = {}

    if state == 'waiting_age':
        if message.text.isdigit():
            age = int(message.text)
            user_data[chat_id]['age'] = age
            user_state[chat_id] = 'waiting_gender'
            bot.send_message(chat_id,
                             "✅ Отлично!\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                             "👤 **Теперь выбери свой пол:**",
                             parse_mode="Markdown",
                             reply_markup=get_gender_keyboard())
        else:
            bot.send_message(chat_id, "❌ Напиши возраст числом.")

    elif state == 'waiting_gender':
        if message.text in ['♂️ Мужской', '♀️ Женский']:
            user_data[chat_id]['gender'] = message.text
            user_state[chat_id] = 'waiting_height'
            bot.send_message(
                chat_id,
                "✅ Принято!\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "📏 **Твой рост в сантиметрах?**\n\n(например: 175)",
                parse_mode="Markdown",
                reply_markup=remove_keyboard()
            )
        else:
            bot.send_message(chat_id, '❌ Выбери пол из кнопок', reply_markup=get_gender_keyboard())

    elif state == 'waiting_height':
        if message.text.isdigit():
            height = int(message.text)
            user_data[chat_id]['height'] = height
            user_state[chat_id] = 'waiting_weight'
            bot.send_message(
                chat_id,
                "✅ Запомнил!\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "⚖️ **Твой вес в килограммах?**\n\n(например: 70)",
                parse_mode="Markdown"
            )
        else:
            bot.send_message(chat_id, '❌ Напиши рост числом.')

    elif state == 'waiting_weight':
        if message.text.isdigit():
            weight = int(message.text)
            user_data[chat_id]['weight'] = weight
            user_state[chat_id] = 'waiting_activity'
            bot.send_message(
                chat_id,
                "✅ Отлично!\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🏃 **Какой у тебя уровень активности?**",
                parse_mode="Markdown",
                reply_markup=get_activity_keyboard()
            )
        else:
            bot.send_message(chat_id, '❌ Напиши вес числом.')

    elif state == 'waiting_activity':
        if message.text in ACTIVITY:
            user_data[chat_id]['activity'] = message.text
            user_state[chat_id] = 'waiting_goal'
            bot.send_message(
                chat_id,
                "✅ Почти готово!\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🎯 **Какая у тебя цель?**",
                parse_mode="Markdown",
                reply_markup=get_goals_keyboard()
            )
        else:
            bot.send_message(chat_id, '❌ Выбери активность из кнопок', reply_markup=get_activity_keyboard())

    elif state == 'waiting_goal':
        if message.text in GOALS:
            user_data[chat_id]['goal'] = message.text

            result = calculate(user_data[chat_id])

            bot.send_message(
                chat_id,
                format_result(user_data[chat_id], result),
                parse_mode="Markdown",
                reply_markup=remove_keyboard()
            )
            bot.send_message(
                chat_id,
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "👇 **Вернуться в главное меню**",
                reply_markup=get_main_keyboard()
            )

            del user_state[chat_id]
            del user_data[chat_id]
        else:
            bot.send_message(chat_id, '❌ Выбери цель из кнопок', reply_markup=get_goals_keyboard())

    elif chat_id not in user_state.keys():
        if message.text == 'ГАЙД(Тренировки)':
            with open('Тренировки.pdf', 'rb') as pdf:
                bot.send_document(chat_id, pdf, caption='ГАЙД(Тренировки)')
        elif message.text == 'ГАЙД(Масса)':
            with open('Масса.pdf', 'rb') as pdf:
                bot.send_document(chat_id, pdf, caption='ГАЙД(Масса)')
        elif message.text == 'ГАЙД(Сушка)':
            with open('Сушка.pdf', 'rb') as pdf:
                bot.send_document(chat_id, pdf, caption='ГАЙД(Сушка)')
        elif message.text == '🔙 Вернуться в меню':
            start(message)

        elif message.text == '💪 Руки':
            files = ['Бицепс', 'Трицепс', 'Плечи']
            for file in files:
                with open(f'{file}.pdf', 'rb') as pdf:
                    bot.send_document(chat_id, pdf, caption=f'Упражнения({file})')
        elif message.text == '🦵 Ноги':
            with open('Ноги.pdf', 'rb') as pdf:
                bot.send_document(chat_id, pdf, caption='Упражениния(Ноги)')
        elif message.text == '🏋️ Грудь':
            with open('Грудь.pdf', 'rb') as pdf:
                bot.send_document(chat_id, pdf, caption='Упражнения(Грудь)')
        elif message.text == '🧗 Спина':
            with open('Спина.pdf', 'rb') as pdf:
                bot.send_document(chat_id, pdf, caption='Упражнения(Спина)')


bot.polling(none_stop=True)