# All data was publicly available

# in alphabetical order
from aiogram import types, Dispatcher, Bot, executor
from aiogram.types.web_app_info import WebAppInfo
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bs4 import BeautifulSoup
import json
import requests
import randfacts
import sqlite3
import time
import webbrowser

# from translate import Translator                               # bad translation
# tranclator = Translator(from_lang="English",to_lang="russian") # bad translation

API = "" #################################!!!!!!!!!! here should be your key to the telegram bot !!!!!!!!!!#################################

bot = Bot(API)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
PRODUCTS = {}

#############################################################################################################################################

#States section

def Order(input_dictionary, id):
    connection = sqlite3.connect('telegram_database.sql')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS orders(id int auto_increment prime key, name varchar(50), telephone varchar(50), email varchar(50), message varchar(4096))')
    connection.commit()
    cursor.execute("INSERT INTO orders (id, name, telephone, email, message) VALUES ('%s', '%s', '%s', '%s', '%s')" % (id, input_dictionary['name'], input_dictionary['telephone'], input_dictionary['email'], input_dictionary['message']))
    connection.commit()
    cursor.close()
    connection.close()

def Feedback(input_dictionary, id):
    connection = sqlite3.connect('telegram_database.sql')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS feedbacks(id int auto_increment prime key, name varchar(50), message varchar(4096))')
    connection.commit()
    cursor.execute("INSERT INTO feedbacks (id, name, message) VALUES ('%s', '%s', '%s')" % (id, input_dictionary['name'], input_dictionary['feedback']))
    connection.commit()
    cursor.close()
    connection.close()

class Form_order(StatesGroup):
    name = State()
    telephone = State()
    email = State()
    message = State()

@dp.message_handler(state=Form_order.name)
async def form_name(message: types.Message, state: FSMContext):
    time.sleep(0.2)
    if len(message.text) <= 50:
        await state.update_data(name=message.text)
        await message.answer(f"Отлично, {message.text}!✅ теперь введите ваш номер телефона:")
        await Form_order.telephone.set()
    else:
        await message.answer('Количество символов не должно превышать 50!🚧\nПопробуйте ввести еще раз:')
        await Form_order.name.set()

@dp.message_handler(state=Form_order.telephone)
async def form_telephone(message: types.Message, state: FSMContext):
    time.sleep(0.2)
    if len(message.text) <= 50:
        await state.update_data(telephone=message.text)
        await message.answer('Отлично!✅ теперь введите ваш email:')
        await Form_order.email.set()
    else:
        await message.answer('Количество символов не должно превышать 50!🚧\nПопробуйте ввести еще раз:')
        await Form_order.telephone.set()

@dp.message_handler(state=Form_order.email)
async def form_email(message: types.Message, state: FSMContext):
    time.sleep(0.2)
    if len(message.text) <= 50:
        await state.update_data(email=message.text)
        await message.answer('Отлично!✅ теперь введите ваш отзыв:')
        await Form_order.message.set()
    else:
        await message.answer('Количество символов не должно превышать 50!🚧\nПопробуйте ввести еще раз:')
        await Form_order.email.set()

@dp.message_handler(state=Form_order.message)
async def form_message(message: types.Message, state: FSMContext):
    time.sleep(0.2)
    if len(message.text) <= 4090:
        markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Куда пойдем?")
        btn_menu = types.KeyboardButton("Обратно в меню")
        btn_up = types.KeyboardButton("Отзывы и пожелания")
        btn_more = types.KeyboardButton("Заказ")
        markup.add(btn_more, btn_up, btn_menu)
        await state.update_data(message=message.text)
        data = await state.get_data()
        await message.answer(f"Имя: {data['name']}, Телефон: {data['telephone']}, Email: {data['email']}, Заказ:{data['message']}")
        await message.answer('Заказ оформлен успешно!✅✅✅', reply_markup=markup)
        await state.finish()
        Order(data, message.from_user.id)
    else:
        await message.answer('Количество символов не должно превышать 4096!🚧\nПопробуйте ввести еще раз:')
        await Form_order.message.set()

class Form_feedback(StatesGroup):
    name = State()
    feedback = State()

@dp.message_handler(state=Form_feedback.name)
async def Form_Feedback_name(message: types.Message, state: FSMContext):
    time.sleep(0.2)
    if len(message.text) <= 50:
        await state.update_data(name=message.text)
        await message.answer('Отлично!✅ Введите отзыв или предложение:')
        await Form_feedback.feedback.set()
    else:
        await message.answer('Количество символов не должно превышать 50!🚧\nПопробуйте ввести еще раз:')
        await Form_feedback.name.set()

@dp.message_handler(state=Form_feedback.feedback)
async def Form_Feedback_name(message: types.Message, state: FSMContext):
    time.sleep(0.2)
    if len(message.text) <= 4090:
        markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Куда пойдем?")
        btn_menu = types.KeyboardButton("Обратно в меню")
        btn_up = types.KeyboardButton("Заказ")
        btn_more = types.KeyboardButton("Отзывы и пожелания")
        markup.add(btn_more, btn_up, btn_menu)
        await state.update_data(feedback=message.text)
        data = await state.get_data()
        await message.answer(f"Имя: {data['name']}, Отзыв или предложение: {data['feedback']}")
        await message.answer('Отзыв или предложение оставлено успешно!✅✅✅', reply_markup=markup)
        await state.finish()
        Feedback(data, message.from_user.id)
    else:
        await message.answer('Количество символов не должно превышать 4096!🚧\nПопробуйте ввести еще раз:')
        await Form_feedback.feedback.set()

#############################################################################################################################################
# commands section

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btn_site = types.InlineKeyboardButton('📲Перейти на сайт-базы💻', url = "http://gfcc.ru/")
    btn_help = types.InlineKeyboardButton('🔊О нас🔊', callback_data='we')
    btn_what_can_do = types.InlineKeyboardButton('⁉Что я умею?🤔', callback_data='cycle')
    markup.row(btn_what_can_do,btn_help)
    markup.row(btn_site)
    file = open('photos/Start_flowers.jpg', 'rb')
    await message.answer_photo(file, f'<strong>Привет, {message.from_user.first_name} {message.from_user.last_name}!</strong>\nЭто цветочный бот!!!\nДля того чтобы посмотреть функционал нажмите на кнопки!', parse_mode='html', reply_markup=markup)

@dp.message_handler(commands=["about_me"])
async def me(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn_menu = types.KeyboardButton('Обратно в меню')
    markup.add(btn_menu)
    await message.answer(message, reply_markup=markup)

@dp.message_handler(commands=["site", "website"])
async def me(message: types.Message):
    await message.answer('Открываем сайт базы данных...')
    time.sleep(0.2)
    webbrowser.open(url='http://gfcc.ru/')

@dp.message_handler(commands=['git', 'github'])
async def open_git(message):
    await message.reply('Открываем сайт...')
    time.sleep(0.5)
    webbrowser.open("https://github.com/LeonardCaceres")

@dp.message_handler(commands=['orders'])
async def orders_com(message: types.Message):
    try:
        connection = sqlite3.connect('telegram_database.sql')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS orders(id int auto_increment prime key, name varchar(50), telephone varchar(50), email varchar(50), message varchar(4096))')
        connection.commit()
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        info = ''
        for el in orders:
            info += f'{el[0]}\n{el[1]}\n{el[2]}\n{el[3]}\n{el[4]}'
        cursor.close()
        connection.close()
        await message.answer(info, reply_markup=types.ReplyKeyboardRemove())
        await message.answer(orders)
    except Exception:
        await message.answer('База данных пуста📝')

@dp.message_handler(commands=['feedbacks'])
async def feedbacks(message: types.Message):
    try:
        connection = sqlite3.connect('telegram_database.sql')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS feedbacks(id int auto_increment prime key, name varchar(50), message varchar(4096))')
        connection.commit()
        cursor.execute('SELECT * FROM feedbacks')
        feedbacks = cursor.fetchall()
        info = ''
        for el in feedbacks:
            info += f'{el[0]}\n{el[1]}\n{el[2]}'
        cursor.close()
        connection.close()
        await message.answer(info, reply_markup=types.ReplyKeyboardRemove())
        await message.answer(feedbacks)
    except Exception:
        await message.answer('База данных пуста📝')

#############################################################################################################################################
# callback section

@dp.callback_query_handler(text="we")
async def help(callback: types.CallbackQuery):
    edit_markup = types.InlineKeyboardMarkup()
    await callback.message.edit_reply_markup(reply_markup=edit_markup)
    markup = types.InlineKeyboardMarkup()
    btn_start_use = types.InlineKeyboardButton('🧑‍💻Нажмите чтобы посмотреть возможности данного бота👩‍💻', callback_data='cycle')
    markup.add(btn_start_use)
    photo_about = open('photos/about_me.jpg', 'rb')
    await callback.message.answer_photo(photo_about, "🌊Бот сделан для того чтобы показать свои навыки в создании телеграмм-ботов и парсинга данных.\n/git - для того чтобы открыть гитхаб🚀", reply_markup=markup)

@dp.callback_query_handler(text="wiki")
async def wiki(callback: types.CallbackQuery):
    edit_markup = types.InlineKeyboardMarkup()
    await callback.message.edit_reply_markup(reply_markup=edit_markup)
    file = open('photos/wiki.jpg', 'rb')
    category = callback.message.text.split(':')[0].split()[0]
    if category == 'Сопутствующие':
        category = callback.message.text.split(':')[0].split()[2]
    try:
        url = f'https://ru.wikipedia.org/wiki/{category}'
        req = requests.get(url=url)
        src = req.text
        soup = BeautifulSoup(src,"lxml")
        info = soup.find('p').text
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_web = types.InlineKeyboardButton("🖥Посмотреть об этом в 'окошке' Википедии🗣",web_app=WebAppInfo(url=url), callback_data= 'web')
        btn_yandex = types.InlineKeyboardButton("🖥Посмотреть об этом в 'окошке' Яндекса🗣", web_app=WebAppInfo(url=f"https://yandex.ru/search/?text={category}"), callback_data= 'web')
        btn_exit = types.InlineKeyboardButton("Выйти из информации о продуктах", callback_data='cycle')
        markup.add(btn_web, btn_yandex, btn_exit)
        await callback.message.answer_photo(file, info, reply_markup= markup)
    except Exception:
        await callback.message.answer('упс... что-то пошло не так🥺')

@dp.callback_query_handler(text='cycle')
async def cycle(callback: types.CallbackQuery):
    edit_markup = types.InlineKeyboardMarkup()
    await callback.message.edit_reply_markup(reply_markup=edit_markup)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Что я могу для вас сделать?")
    btn_product = types.KeyboardButton('Расскажите о своих продуктах')
    btn_feedback = types.KeyboardButton('Хочу оформить заказ или оставить отзыв')
    btn_dino = types.KeyboardButton('Включи игру про динозаврика', web_app=WebAppInfo(url='https://dino-chrome.com/ru'))
    btn_randfact = types.KeyboardButton('Расскажи рандомный факт')
    markup.add(btn_product, btn_feedback, btn_dino, btn_randfact)
    file = open('photos/cycle.jpg', 'rb')
    await callback.message.answer_photo(file, '<b><strong>Вы находитесь в меню:</strong></b>\nЧто я могу для вас сделать?:\n1)Показать наличие товаров магазина <b>Golden Flowers</b>\n2)Оставить отзыв или заказ(<b>Golden Flowers</b>)\n3)Включить игру про динозаврика\n4)Найти интересный факт\n5)/site - перейти на сайт базы данных', parse_mode='html', reply_markup=markup)

@dp.callback_query_handler(text="products")
async def products(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    markup_delete = types.ReplyKeyboardRemove()
    await callback.message.reply('⏳Секунду...', reply_markup=markup_delete)
    time.sleep(1)
    await bot.delete_message(callback.message.chat.id, callback.message.message_id + 1)
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Выберите категорию цветов")
    btn1 = types.KeyboardButton('Срезанные цветы')
    btn2 = types.KeyboardButton('Горшечные растения')
    btn3 = types.KeyboardButton('Аксессуары')
    btn_exit = types.KeyboardButton('Обратно в меню')
    markup.add(btn1, btn2, btn3, btn_exit)
    await callback.message.answer('Существует <b><em>3</em></b> категории <strong>товаров</strong>:\n<b><strong>•Срезанные цветы\n•Горшечные растения\n•Аксессуары</strong></b>\nВыберете категорию:', parse_mode='html', reply_markup=markup)

@dp.callback_query_handler(text = "fact")
async def fact(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_fact = types.InlineKeyboardButton('Еще интересный факт!', callback_data='fact')
    btn_up = types.InlineKeyboardButton('Обратно в меню', callback_data='cycle')
    btn_interpreter = types.InlineKeyboardButton('Открыть переводчик', url = 'https://translate.yandex.ru/?from=tabbar&source_lang=en&target_lang=ru')
    markup.add(btn_fact, btn_interpreter, btn_up)
    await callback.message.answer(randfacts.get_fact(), reply_markup=markup)

@dp.callback_query_handler()
async def all_callback(callback: types.CallbackQuery):
    edit_markup = types.InlineKeyboardMarkup()
    await callback.message.edit_reply_markup(reply_markup=edit_markup)
    with open('info_dict.json', encoding="utf-8") as file:
        product_info = json.load(file)
    with open("data/cut_flowers.json", encoding="utf-8") as file:
        cut_flowers = json.load(file)
    with open('data/right_name_cut.txt', encoding="utf-8") as file:
        cut_names = file.read()
    with open("data/potted_flowers.json", encoding="utf-8") as file:
        potted_flowers = json.load(file)
    with open('data/right_name_potted.txt', encoding="utf-8") as file:
        potted_names = file.read()
    with open("data/access_flowers.json", encoding="utf-8") as file:
        access_flowers = json.load(file)
    with open('data/right_name_access.txt', encoding="utf-8") as file:
        access_names = file.read()
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_wiki = types.InlineKeyboardButton('🔭Узнать о подкатегории товара📡', callback_data='wiki')
    btn_exit = types.InlineKeyboardButton("Выйти из информации о товарах", callback_data='cycle')
    btn_products = types.InlineKeyboardButton('Еще о товарах',callback_data='products')
    markup.add(btn_wiki, btn_products, btn_exit)
    markup_exit = types.InlineKeyboardMarkup()
    markup_exit.add(btn_exit)
    if callback.data in cut_names.split('\n'):
        if product_info[cut_flowers[callback.data]] != "Страница пуста":
            await callback.message.answer(f'В следующем сообщении :\nтовары в наличии в отсортированном списке:')
            text_mes = callback.data + ':\n' + '\n'.join(product_info[cut_flowers[callback.data]])
            if len(text_mes) > 4095:
                if len(text_mes) > 8160:
                    await callback.message.answer(text_mes[:4090])
                    await callback.message.answer(text_mes[4090:8160])
                    await callback.message.answer(callback.data + ':\n' + text_mes[8160:], reply_markup=markup)
                else:
                    await callback.message.answer(text_mes[:4095])
                    await callback.message.answer(callback.data + ':\n' + text_mes[4095:], reply_markup=markup)
            else:
                await callback.message.answer(text_mes, reply_markup=markup)
        else:
            photo_no = open('photos/not_on_sale.jpg', 'rb')
            await callback.message.answer_photo(photo_no, f"К сожалению, в этой категории({callback.data}) отсутсвуют товары", reply_markup=markup_exit)
    if callback.data in potted_names.split('\n'):
        if product_info[potted_flowers[callback.data]] != "Страница пуста":
            await callback.message.answer(f'В следующем сообщении :\nтовары в наличии в отсортированном списке:')
            text_mes = callback.data + ':\n' + '\n'.join(product_info[potted_flowers[callback.data]])
            if len(text_mes) > 4096:
                if len(text_mes) > 4095 * 2:
                    await callback.message.answer(text_mes[:4095])
                    await callback.message.answer(text_mes[4095:4095 * 2])
                    await callback.message.answer(callback.data + ':\n' + text_mes[4095 * 2:], reply_markup=markup)
                else:
                    await callback.message.answer(text_mes[:4095])
                    await callback.message.answer(callback.data + ':\n' + text_mes[4095:],reply_markup=markup)
            else:
                await callback.message.answer(text_mes,reply_markup=markup)
        else:
            photo_no = open('photos/not_on_sale.jpg', 'rb')
            await callback.message.answer_photo(photo_no, f"К сожалению, в этой категории({callback.data}) отсутсвуют товары", reply_markup=markup_exit)
    if callback.data in access_names.split('\n'):
        if product_info[access_flowers[callback.data]] != "Страница пуста":
            await callback.message.answer(f'В следующем сообщении :\nтовары в наличии в отсортированном списке:')
            text_mes = callback.data + ':\n' + '\n'.join(product_info[access_flowers[callback.data]])
            if len(text_mes) > 4096:
                if len(text_mes) > 4095 * 2:
                    await callback.message.answer(text_mes[:4095])
                    await callback.message.answer(text_mes[4095:4095 * 2])
                    await callback.message.answer(callback.data + ':\n' + text_mes[4095 * 2:], reply_markup=markup)
                else:
                    await callback.message.answer(text_mes[:4095])
                    await callback.message.answer(callback.data + ':\n' + text_mes[4095:], reply_markup=markup)
            else:
                await callback.message.answer(text_mes, reply_markup=markup)
        else:
            photo_no = open('photos/not_on_sale.jpg', 'rb')
            await callback.message.answer_photo(photo_no, f"К сожалению, в этой категории({callback.data}) отсутсвуют товары", reply_markup=markup_exit)

#############################################################################################################################################

# text section

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def media(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    btn_menu = types.KeyboardButton("Обратно в меню")
    markup.add(btn_menu)
    await message.answer('К сожалению, я всего лишь текстовый бот и могу только любоваться вашими фотографиями при вашей отправке мне(((', reply_markup=markup)

@dp.message_handler(content_types=types.ContentTypes.AUDIO)
async def audio(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    btn_menu = types.KeyboardButton("Обратно в меню")
    markup.add(btn_menu)
    await message.answer('К сожалению, я всего лишь текстовый бот и могу только слушать ваши аудио при вашей отправке мне(((', reply_markup=markup)

@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def document(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    btn_menu = types.KeyboardButton("Обратно в меню")
    markup.add(btn_menu)
    await message.answer('К сожалению, я всего лишь текстовый бот и могу только читать ваши файлы при вашей отправке мне(((', reply_markup=markup)

@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    global PRODUCTS
    btn_products = types.InlineKeyboardButton('Обратно к категориям', callback_data='products')
    btn_menu = types.InlineKeyboardButton("Выйти из информации о продуктах", callback_data='cycle')
    if message.text.lower() == "расскажи рандомный факт":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_fact = types.InlineKeyboardButton('Еще интересный факт!',callback_data= 'fact')
        btn_up = types.InlineKeyboardButton('Обратно в меню', callback_data='cycle')
        btn_interpreter = types.InlineKeyboardButton('Открыть переводчик',
                                                     url='https://translate.yandex.ru/?from=tabbar&source_lang=en&target_lang=ru')
        markup.add(btn_fact, btn_interpreter, btn_up)
        await message.answer(randfacts.get_fact(), reply_markup=markup)
    elif message.text.lower() == 'расскажите о своих продуктах':
        markup_delete = types.ReplyKeyboardRemove()
        await message.reply('⏳Секунду...',reply_markup=markup_delete)
        time.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Выберите категорию цветов")
        btn1 = types.KeyboardButton('Срезанные цветы')
        btn2 = types.KeyboardButton('Горшечные растения')
        btn3 = types.KeyboardButton('Аксессуары')
        btn_exit = types.KeyboardButton('Обратно в меню')
        markup.add(btn1,btn2,btn3,btn_exit)
        await message.answer('Существует <b><em>3</em></b> категории <strong>товаров</strong>:\n<b><strong>•Срезанные цветы\n•Горшечные растения\n•Аксессуары</strong></b>\nВыберете категорию:', parse_mode='html',reply_markup=markup)
    elif message.text.lower() == 'срезанные цветы':
        markup_delete = types.ReplyKeyboardRemove()
        await message.reply('⏳Секунду...', reply_markup=markup_delete)
        time.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        with open('data/names.txt', encoding="utf-8") as file:
            names = file.readlines()
        strings = ''
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, name in enumerate(names):
            if i == 10:
                break
            right_name = name[17:].replace('__', ' ').replace('_', ' ')
            btn_name = right_name.replace('\n','')
            markup.add(types.InlineKeyboardButton(f"{btn_name}",callback_data=str(btn_name)))
            strings += right_name
            PRODUCTS[btn_name] = name.replace('\n','')
        markup.add(btn_products, btn_menu)
        photo_cut = open('photos/cut.jpg', 'rb')
        await message.answer_photo(photo_cut, "В категории  'Срезанные цветы' есть 10 подкатегорий:\nВыберите одну из интересующих подкатегорий:", reply_markup=markup)
        # await message.answer(strings)
        # with open('data/right_name_cut.txt','w',encoding='utf-8') as file:
        #     file.write(strings)
        # with open('data/cut_flowers.json', 'w',encoding="utf-8") as file:
        #     json.dump(PRODUCTS, file, indent=4, ensure_ascii=False)
    elif message.text.lower() == 'горшечные растения':
        markup_delete = types.ReplyKeyboardRemove()
        await message.reply('⏳Секунду...', reply_markup=markup_delete)
        time.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        with open('data/names.txt', encoding="utf-8") as file:
            names = file.readlines()
        strings = ''
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, name in enumerate(names):
            if i < 10:
                continue
            if i == 24:
                break
            right_name = name[20:].replace('__', ' ').replace('_', ' ')
            btn_name = right_name.replace('\n', '')
            markup.add(types.InlineKeyboardButton(f"{btn_name}", callback_data=str(btn_name)))
            strings += right_name
            PRODUCTS[btn_name] = name.replace('\n', '')
        markup.add(btn_products, btn_menu)
        photo_potted = open('photos/potted.jpg', 'rb')
        await message.answer_photo(photo_potted, "В категории 'Горшечные растения' есть 14 подкатегорий:\nВыберите одну из интересующих подкатегорий:", reply_markup=markup)
        # await message.answer(strings)
        # with open('data/right_name_potted.txt','w',encoding='utf-8') as file:
        #     file.write(strings)
        # with open('data/potted_flowers.json', 'w',encoding="utf-8") as file:
        #     json.dump(PRODUCTS, file, indent=4, ensure_ascii=False)
    elif message.text.lower() == 'аксессуары':
        markup_delete = types.ReplyKeyboardRemove()
        await message.reply('⏳Секунду...', reply_markup=markup_delete)
        time.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        with open('data/names.txt', encoding="utf-8") as file:
            names = file.readlines()
        strings = ''
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, name in enumerate(names):
            if i < 25:
                continue
            right_name = name[12:].replace('__', ' ').replace('_', ' ')
            btn_name = right_name.replace('\n', '')
            markup.add(types.InlineKeyboardButton(f"{btn_name}", callback_data=str(btn_name)))
            strings += right_name
            PRODUCTS[btn_name] = name.replace('\n', '')
        markup.add(btn_products, btn_menu)
        photo_access = open('photos/access.jpg', 'rb')
        await message.answer_photo(photo_access, "В Категории 'Акссесуары' есть 10 подкатегорий:\nВыберите одну из интересующих подкатегорий:", reply_markup=markup)
        # await message.answer(strings)
        # with open('data/right_name_access.txt','w',encoding='utf-8') as file:
        #     file.write(strings)
        # with open('data/access_flowers.json', 'w',encoding="utf-8") as file:
        #     json.dump(PRODUCTS, file, indent=4, ensure_ascii=False)
    elif message.text.lower() == 'обратно в меню':
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Что я могу для вас сделать?")
        btn_product = types.KeyboardButton('Расскажите о своих продуктах')
        btn_feedback = types.KeyboardButton('Хочу оформить заказ или оставить отзыв')
        btn_dino = types.KeyboardButton('Включи игру про динозаврика', web_app=WebAppInfo(url='https://dino-chrome.com/ru'))
        btn_randfact = types.KeyboardButton('Расскажи рандомный факт')
        markup.add(btn_product, btn_feedback, btn_dino, btn_randfact)
        file = open('photos/cycle.jpg', 'rb')
        await message.answer_photo(file, '<b><strong>Вы находитесь в меню:</strong></b>\nЧто я могу для вас сделать?:\n1)Показать наличие товаров магазина <b>Golden Flowers</b>\n2)Оставить отзыв или заказ(<b>Golden Flowers</b>)\n3)Включить игру про динозаврика\n4)Найти интересный факт\n5)/site - перейти на сайт базы данных', parse_mode='html', reply_markup=markup)
    elif message.text.lower() == 'хочу оформить заказ или оставить отзыв':
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Что вы хотите?(отзыв или заказ)")
        btn1 = types.KeyboardButton('Отзывы и пожелания')
        btn2 = types.KeyboardButton('Заказ')
        markup.add(btn1, btn2)
        await message.answer('Что вы конкретно хотите сделать?', reply_markup=markup)
    elif message.text.lower() == 'заказ':
        await message.answer('Введите своё имя(длина < 50):', reply_markup= types.ReplyKeyboardRemove())
        await Form_order.name.set()
    elif message.text.lower() == 'отзывы и пожелания':
        await message.answer('Введите своё имя(длина < 50):', reply_markup= types.ReplyKeyboardRemove())
        await Form_feedback.name.set()
    else:
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        btn_menu = types.KeyboardButton("Обратно в меню")
        markup.add(btn_menu)
        await message.answer('Я вас не понимаю((\nПредлагаю вам перейти в меню!〽', reply_markup=markup)

@dp.message_handler()
async def all_messages(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    btn_menu = types.KeyboardButton("Обратно в меню")
    markup.add(btn_menu)
    await message.answer('Потрясающе!!🐼, только я не могу это прочитать(((🥺', reply_markup=markup)

#############################################################################################################################################

executor.start_polling(dp)