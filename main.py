from aiogram import Dispatcher, executor, Bot
from states import Registration, GetProduct, Cart, Order
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import database
import states
import buttons as btns
from datetime import datetime

bot = Bot('5870589260:AAGmhrWzHUEqDhJ04sMqiYTHzZJzAAW7Zas')

dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start_message(message):

    user_id = message.from_user.id

    checker = database.check_user(user_id)
    if checker:
        await message.answer(f'Привет, {message.from_user.last_name},\n\nЯ рада снова видеть Вас у себя в боте. По всем вопросам можете обратится:  @photofelizss'
                             f'\n\n Выберите раздел🔽',
                             reply_markup=btns.main_menu())
    else:
        await message.answer(
            f'Приветствую Вас {message.from_user.first_name}\n\n Давайте знакомиться!\n\nОтправьте Имя для регистрации!',
            reply_markup=btns.ReplyKeyboardMarkup())

        await Registration.getting_name_state.set()


@dp.message_handler(state=Registration.getting_name_state)
async def get_username(message, state=Registration.getting_name_state):

    user_answer = message.text

    await state.update_data(name=user_answer)
    await message.answer('Красивое имя!\n\nОтправьте теперь номер телефона!', reply_markup=btns.phone_number_kb())

    await Registration.getting_phone_number.set()

@dp.message_handler(state=Registration.getting_phone_number, content_types=['contact'])
async def get_number(message, state=Registration.getting_phone_number):

    user_answer = message.contact.phone_number


    await state.update_data(number=user_answer)
    await message.answer('Номер получила!\n\nВыберите пол', reply_markup=btns.gender_kb())


    await Registration.getting_gender.set()

@dp.message_handler(state=Registration.getting_gender)
async def get_gender(message, state=Registration.getting_gender):

    user_answer = message.text
    await message.answer('Знакомство прошло успешно❤️!\n\nВыберите раздел🔽', reply_markup=btns.main_menu())

    all_info = await state.get_data()
    name = all_info.get('name')
    phone_number = all_info.get('number')
    latitude = all_info.get('latitude')
    longitude = all_info.get('longitude')
    gender = user_answer
    user_id = message.from_user.id
    database.add_user(user_id, name, phone_number, gender)

    await state.finish()


@dp.message_handler(state=GetProduct.getting_pr_name, content_types=['text'])
async def select_count(message):
    user_answer = message.text
    user_id = message.from_user.id

    user_data = await dp.current_state(user=user_id).get_data()
    category_id = user_data.get('category_id')

    actual_products = [i[0] for i in database.get_name_product(category_id)]


    if user_answer == 'Назад◀️':
        await message.answer('Выберите категорию', reply_markup=btns.catalog_folder())

        await dp.current_state(user=user_id).finish()

    elif user_answer in actual_products:
        product_info = database.get_all_info_product(user_answer)
        if 'торт' in user_answer.lower():
            await bot.send_photo(user_id, photo=product_info[4],
                                 caption=f'{product_info[0]}\n\nЦена: {product_info[2]} \n\nОписание: {product_info[3]}\n\n@photofelizss_bot\n\nВыберите количество',
                                 reply_markup=btns.product_count())

        elif 'Пирожное' in user_answer:
            await bot.send_photo(user_id, photo=product_info[4],
                                 caption=f'{product_info[0]}\n\nЦена: {product_info[2]} \n\nОписание: {product_info[3]}\n\n@photofelizss_bot\n\nВыберите количество',
                                 reply_markup=btns.minicake_count_kb())

        await dp.current_state(user=user_id).update_data(user_product=message.text, price=product_info[2])

        await states.GetProduct.getting_pr_count.set()


@dp.message_handler(state=GetProduct.getting_pr_count)
async def prod_count(message, state=GetProduct.getting_pr_count):
    product_count = message.text
    user_data = await state.get_data()
    user_product = user_data.get('user_product')
    category_id = user_data.get('category_id')
    pr_price = float(user_data.get('price') )


    if product_count.isnumeric():
        database.add_pr_to_cart(message.from_user.id, user_product, pr_price, int(product_count))
        database.add_pr_to_cart2(message.from_user.id, user_product, pr_price, int(product_count))

        await message.answer('Товар добавлен в корзину\n\nВыберите категорию', reply_markup=btns.catalog_folder())
        await state.finish()

    elif message.text != 'Назад◀️':
        await message.answer('Выберите количество используя кнопки', reply_markup=btns.product_count())

    else:
        await message.answer('Выберите товар из списка', reply_markup=btns.count_kb(category_id))
        await states.GetProduct.getting_pr_name.set()


@dp.message_handler(state=Cart.waiting_for_product)
async def cart_function(message, state=Cart.waiting_for_product):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Назад◀️':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
        await dp.current_state(user=message.from_user.id).finish()


    elif user_answer == 'Очистить':

        database.delete_from_cart(user_id)
        await message.answer('Корзина очищена\n\n❗️❗️Нажмите кнопку Назад❗️❗️')

    if user_answer == 'Оформить заказ':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ✅🔽:\n\n'
            admin_message = 'Новый заказ✅✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                admin_message += f'- {i[1]}: \n{i[-1]} шт = {i[3]:}  сум\n\n'
                total_price += i[3]

            result_answer += f' \nИтог:   {total_price:} сум'
        await message.answer('Напишите в виде текста дату "ЗАКАЗА" и "ДОСТАВКИ"!!!\n\nНажмите кнопку "Потвердить"', reply_markup=btns.confirmation_kb())
        await Order.waiting_comment.set()

    # elif user_answer == 'Отправить':
    #     await message.answer('Раздел оформления заказа\n\n'
    #                          'Нажмите одну из кнопок🔽', reply_markup=btns.confirmation_kb())
    #     # if message.text == message.text:
    #     #
    #     #     await bot.forward_message(message.from_user.id)

@dp.message_handler(state=Order.waiting_comment)
async def comment_function(message, state=Order.waiting_comment):
    user_answer = message.text
    user_id = message.from_user.id
    await state.update_data(comment=message.text)
    await message.answer('Нажмите кнопку "Потвердить"',
                         reply_markup=btns.confirmation_kb())

    await Order.waiting_comment_accept.set()

@dp.message_handler(state=Order.waiting_comment_accept)
async def comment_function(message, state=Order.waiting_comment_accept):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Подтвердить':
        order_id = datetime.now().microsecond
        user_cart = database.get_user_cart(message.from_user.id)
        user_data = await state.get_data()

        user_comment = user_data.get('comment')
        if user_cart:

            result_answer = f'Ваш заказ №{order_id} :\n\n'
            admin_message = f'Новый заказ {order_id} :\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                admin_message += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                total_price += i[3]

            result_answer += f' \nИтог:   {total_price:} сум'
            admin_message += f'Номер телефона: {i[2]}\n\nИтог:   {total_price:} сум'
            admin_message += f'\n\n_________________\n\nКоментарий: {user_comment}'

            # ---Отправка пользователю
            await message.answer(result_answer, reply_markup=btns.main_menu())
            await message.answer('Успешно оформлен✅\n\n')
            await state.finish()
            await bot.send_message(140566, admin_message)
            database.delete_from_cart(user_id)

@dp.message_handler(content_types=['text'])
async def main_menu(message):
    user_answer = message.text
    user_id = message.from_user.id


    if user_answer == 'Корзина':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваша корзина🗑:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                total_price += i[3]

            result_answer += f' \nИтог:   {total_price:} сум'
            await message.answer(result_answer, reply_markup=btns.cart_kb())
            await Cart.waiting_for_product.set()


    if user_answer == 'Каталог':
        await message.answer('Выберите категорию🔽', reply_markup=btns.catalog_folder())

    elif user_answer == 'Назад🔙':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())

    if user_answer == 'Торт':
        await dp.current_state(user=user_id).update_data(category_id=11)
        await message.answer('Выберите продукт🔽', reply_markup=btns.cake_kb())
        await states.GetProduct.getting_pr_name.set()

    elif user_answer == 'Пирожное':
        await dp.current_state(user=user_id).update_data(category_id=22)
        await message.answer('Выберите продукт🔽', reply_markup=btns.minicake_kb())
        await states.GetProduct.getting_pr_name.set()

    elif user_answer == 'Корзина':
        await message.answer('Выберите кнопку')

    if user_answer == 'Назад◀️':
        await message.answer('Выберите категорию🔽', reply_markup=btns.catalog_folder())

    elif user_answer == 'О нас':
        await message.answer(about)

    elif user_answer == 'Контакты':
        await message.answer(f'📞 Телефон:\n+998998250055 \n\nTelegram: @photofelizss')



    elif user_answer == 'Список заказов':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ✅:\n\n'

            admin_message = 'Новый заказ✅:\n\n'

            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'

                admin_message += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'

                total_price += i[3]

            result_answer += f' \nИтог:   {total_price:} сум'
            admin_message += f' Номер телефона: {i[2]}\n\nИтог:   {total_price:} сум'

            await message.answer(result_answer, reply_markup=btns.order_kb())

            await Order.waiting_accept.set()

        elif user_answer == 'Назад◀️':
            await message.answer('❗️Вы вернулись в Главное меню ActiveBee❗️\n\nВыберите раздел🔽',
                                 reply_markup=btns.main_menu())

        else:

            await message.answer('Ваша корзина пустая🗑\n\n'

                                 'Для выбора продукта нажмите кнопку ❗️Каталог❗️')


@dp.message_handler(state=Order.waiting_accept)
async def accept_order(message):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Назад◀️':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
        await dp.current_state(user=message.from_user.id).finish()

    elif user_answer == 'Оформить заказ':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ✅:\n\n'
            admin_message = 'Новый заказ✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                admin_message += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                total_price += i[3]

            admin_message += f'Номер телефона: {i[2]}\n\nИтог:   {total_price:} сум'
            result_answer += f' \nИтог:   {total_price:} сум'

            await message.answer(result_answer, reply_markup=btns.main_menu())
            print(user_cart)
            await message.answer('Успешно оформлен✅\n\n')
            await bot.send_message(140566, admin_message)
            await dp.current_state(user=message.from_user.id).finish()
            database.delete_from_cart(user_id)



    elif user_answer == 'Список заказов':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ✅:\n\n'
            admin_message = 'Новый заказ✅:\n\n'
            # total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                admin_message += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                total_price += i[3]

            admin_message += f'-Номер телефона: {i[2]}\n\nИтог:   {total_price:} сум'

            await message.answer(result_answer, reply_markup=btns.order_kb())

            await Order.waiting_accept.set()

        else:
            await message.answer('Ваша корзина пустая🗑\n\n'
                                 'Для выбора продукта нажмите кнопку <Каталог>')

# Order list
@dp.message_handler(state=Order.waiting_accept)
async def accept_order(message):
    user_answer = message.text
    user_id = message.from_user.id
    if user_answer == 'Назад◀️':
        await message.answer('❗Вы вернулись в Главное меню ActiveBee❗️\n\nВыберите раздел🔽', reply_markup=btns.main_menu())
        await dp.current_state(user=message.from_user.id).finish()

    elif user_answer == 'Оформить заказ':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ✅:\n\n'
            admin_message = 'Новый заказ✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                admin_message += f'- {i[1]}: \n{i[-1]} шт = {i[3]:} сум\n\n'
                total_price += i[3]

            admin_message += f'Номер телефона: {i[2]}\n\nИтог:   {total_price:} сум'
            result_answer += f'Итог:   {total_price:} сум'

            await message.answer(result_answer, reply_markup=btns.main_menu())
            print(user_cart)
            await message.answer('Успешно оформлен✅\n\n')
            await bot.send_message(140566, admin_message)
            await dp.current_state(user=message.from_user.id).finish()
            database.delete_from_cart(user_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)