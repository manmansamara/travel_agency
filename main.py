import telebot
from telebot import types
import pymysql

# Подключение к MySQL
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',  # замените вашими данными
        password='',  # замените вашим паролем
        db='agency',  # замените вашей базой данных
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
except Exception as e:
    print(f"Произошла ошибка при подключении к базе данных: {e}")

# Токен вашего Телеграм-бота
TOKEN = '8256969049:AAFPr55ZNlQR1IL2qifbxFBcBqU8y_n0Deo'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn_website = types.KeyboardButton('🌐 Наш сайт')
    btn_tours = types.KeyboardButton('🌍 Наши туры')
    btn_booking = types.KeyboardButton('🛩 Забронировать тур')
    
    markup.add(btn_website, btn_tours, btn_booking)
    
    welcome_text = f'🌟 Приветствуем вас в нашей туристической компании!\n\nМы предлагаем увлекательные путешествия по всему миру.\nИспользуйте меню ниже:'
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Обработчик кнопки "Наш сайт"
@bot.message_handler(func=lambda message: message.text == '🌐 Наш сайт')
def website_button(message):
    try:
        bot.reply_to(message, 'Посмотрите наши услуги на сайте: https://manmansamara.github.io/travel_agency/')
    except Exception as e:
        bot.reply_to(message, f'Ошибка при обработке вашего запроса: {e}')

# Обработчик кнопки "Наши туры"
@bot.message_handler(func=lambda message: message.text == '🌍 Наши туры')
def show_tours(message):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tours;"
            cursor.execute(sql)
            results = cursor.fetchall()
        
        # Формируем Inline-клавиатуру с названием туров
        keyboard = types.InlineKeyboardMarkup()
        buttons = []
        for tour in results:
            button = types.InlineKeyboardButton(text=f'🌍 {tour["name"]}', callback_data=f'tour_{tour["tour_id"]}')
            buttons.append(button)
        keyboard.add(*buttons)
        
        bot.send_message(message.chat.id, 'Выберите интересующий Вас тур:', reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, f'Ошибка при получении данных о турах: {e}')

# Обработчик обратных вызовов (callback queries) для просмотра туров
@bot.callback_query_handler(func=lambda call: call.data.startswith('tour_'))
def tour_callback(call):
    try:
        tour_id = int(call.data.split('_')[1])  # извлекаем ID выбранного тура
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tours WHERE tour_id=%s;"
            cursor.execute(sql, (tour_id,))
            result = cursor.fetchone()
        
        # Отправляем полную информацию о выбранном туре
        info = f'''🌍 Название тура: {result["name"]}
⏳ Продолжительность: {result["duration"]}
🚀 Направление: {result["from_where"]}
💸 Цена: {result["price"]} руб.
🖼️ Ссылка на буклет: {result["image_place"]}
'''
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Посмотреть другие 🌍", callback_data='show_tours'))
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, reply_markup=keyboard)
    except Exception as e:
        bot.answer_callback_query(callback_query_id=call.id, text="Что-то пошло не так.")

# Обработчик кнопки "Забронировать тур"
@bot.message_handler(func=lambda message: message.text == '🛩 Забронировать тур')
def booking_button(message):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tours;"
            cursor.execute(sql)
            results = cursor.fetchall()
        
        # Формируем Inline-клавиатуру с названием туров
        keyboard = types.InlineKeyboardMarkup()
        buttons = []
        for tour in results:
            button = types.InlineKeyboardButton(text=f'🛩 {tour["name"]}', callback_data=f'book_{tour["tour_id"]}')
            buttons.append(button)
        keyboard.add(*buttons)
        
        bot.send_message(message.chat.id, 'Выберите тур для бронирования:', reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, f'Ошибка при получении данных о турах: {e}')

# Обработчик обратных вызовов (callback queries) для бронирования туров
@bot.callback_query_handler(func=lambda call: call.data.startswith('book_'))
def book_tour(call):
    try:
        tour_id = int(call.data.split('_')[1])  # извлекаем ID выбранного тура
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tours WHERE tour_id=%s;"
            cursor.execute(sql, (tour_id,))
            result = cursor.fetchone()
        
        # Запрашиваем имя пользователя
        bot.send_message(call.message.chat.id, 'Введите ваше имя:')
        bot.register_next_step_handler(call.message, get_name, tour_id)
    except Exception as e:
        bot.answer_callback_query(callback_query_id=call.id, text="Что-то пошло не так.")

# Получаем имя пользователя
def get_name(message, tour_id):
    name = message.text
    bot.send_message(message.chat.id, 'Введите ваши пожелания:')
    bot.register_next_step_handler(message, get_description, tour_id, name)

# Получаем описание заказа
def get_description(message, tour_id, name):
    description = message.text
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO orders (who, description, datetime, tour_number) VALUES (%s, %s, NOW(), %s);"
            cursor.execute(sql, (name, description, tour_id))
            connection.commit()
        
        bot.send_message(message.chat.id, 'Ваш заказ успешно оформлен! Скоро с вами свяжутся наши сотрудники. Спасибо за выбор нашей компании!')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при оформлении заказа: {e}')

# Обработчик кнопки "Посмотреть другие"
@bot.callback_query_handler(func=lambda call: call.data == 'show_tours')
def show_tours_callback(call):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tours;"
            cursor.execute(sql)
            results = cursor.fetchall()
        
        # Формируем Inline-клавиатуру с названием туров
        keyboard = types.InlineKeyboardMarkup()
        buttons = []
        for tour in results:
            button = types.InlineKeyboardButton(text=f'🌍 {tour["name"]}', callback_data=f'tour_{tour["tour_id"]}')
            buttons.append(button)
        keyboard.add(*buttons)
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите интересующий Вас тур:', reply_markup=keyboard)
    except Exception as e:
        bot.answer_callback_query(callback_query_id=call.id, text="Что-то пошло не так.")

# Запускаем бесконечный цикл приёма сообщений
bot.polling(none_stop=True)