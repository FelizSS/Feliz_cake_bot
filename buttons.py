from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


import database

def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Поделиться контактом', request_contact=True)
    kb.add(button)

    return kb

def gender_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Мужчина')
    button1 = KeyboardButton('Женщина')
    kb.add(button, button1)

    return kb

def product_count():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [KeyboardButton(i) for i in range(1, 4)]
    back = KeyboardButton('Назад◀️')
    kb.add(*buttons)
    kb.add(back)

    return kb

def count_kb(category_id):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад◀️')
    all_products = database.get_name_product(category_id)
    #print(all_products)

    #Генерируем список кнопок с названием продуктов
    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Каталог')
    order = KeyboardButton('Список заказов')
    cart = KeyboardButton('Корзина')
    callback = KeyboardButton('Контакты')

    kb.add(button, order, cart, callback)

    return kb

def catalog_folder():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    cake = KeyboardButton('Торт')
    minicake = KeyboardButton('Пирожное')
    cart = KeyboardButton('Корзина')
    back = KeyboardButton('Назад🔙')

    kb.add(cake, minicake, cart, back)

    return kb

def cake_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад◀️')
    all_products = database.cake_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)
    return kb


def minicake_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = KeyboardButton('Назад◀️')
    all_products = database.mini_cake_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)
    return kb

def minicake_count_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [KeyboardButton(str(i)) for i in range(6,11,2)]
    button = KeyboardButton('Назад◀️')

    kb.add(*buttons, button)
    return kb


def cart_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = KeyboardButton('Очистить')
    button1 = KeyboardButton('Оформить заказ')
    back = KeyboardButton('Назад◀️')
    kb.add(button1, button, back)

    return kb

def confirmation_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Подтвердить')
    button2 = KeyboardButton('Назад◀️')
    kb.add(button, button2)

    return kb

def order_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # button = KeyboardButton('Наличные')
    button1 = KeyboardButton('Оформить заказ')
    back = KeyboardButton('Назад◀️')
    kb.add(button1, back)

    return kb

def comment_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    comment = KeyboardButton('Отправить')
    back = KeyboardButton('Назад◀️')
    kb.add(comment, back)

    return kb



