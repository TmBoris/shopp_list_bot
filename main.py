# list of all products
import re
from aiogram import types, executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import pymorphy2
from config import TOKEN_API
from keyboards import *
import sqlite_db
import sys
import datetime
# Importing platform library
from platform import python_version
# Getting Python interpreter version as a result
print("Current Version of Python interpreter we are using-", python_version())
print(sys.version)
bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot,
                storage=storage)


class ProductStatesGroup(StatesGroup):
    title = State()
    # photo = State()
    delete = State()
    new_title = State()
    Vtitle = State()
    Vdelete = State()
    Vmenu = State()
    menu = State()
    addmore = State()
    Vaddmore = State()


async def on_startup(_):
    await sqlite_db.db_connect()
    print('Подключение к БД выполнено успешно')


async def show_all_products(message: types.Message, products: list) -> None:
    sum = len(products)
    print(sum)

    if sum > 0:
        arr = '\n'.join(f"{product[0]}) <b>{product[1]}</b>" for product in products)
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Список для Москвы:\n{arr}',
                               parse_mode='HTML')
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='В списке сейчас пусто! Всё купил, умничка!')


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    first_name = str(message.from_user.first_name)
    last_name = str(message.from_user.last_name)
    username = str(message.from_user.username)
    await sqlite_db.reg_new_user(user_id, first_name, last_name, username)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Добро пожаловать!\nЧто хочешь сделать?',
                           reply_markup=get_start_kb_k())
    await ProductStatesGroup.title.set()


# @dp.message_handler(content_types=['text'], state='*')
# async def cmd_start_id(message: types.Message):
#     user_id = message.from_user.id
#     first_name = str(message.from_user.first_name)
#     last_name = str(message.from_user.last_name)
#     username = str(message.from_user.username)
#     await sqlite_db.reg_new_user(user_id, first_name, last_name, username)
#     await bot.send_message(chat_id=message.chat.id,
#                            text=f'Добро пожаловать!\nЧто хочешь сделать?',
#                            reply_markup=get_start_kb_k())
#     #await ProductStatesGroup.title.set()

@dp.message_handler(text='Купить в квартиру', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id,
                           text='Что хочешь сделать со списком?',
                           reply_markup=get_start_kb_k())
    await state.finish()
    await ProductStatesGroup.title.set()


@dp.message_handler(text='Вернуться в меню', state=ProductStatesGroup.title)
async def cb_add_new_product(message: types.Message, state: FSMContext) -> None:
    await message.answer('апчхи',
                         reply_markup=get_start_kb_k())


@dp.message_handler(commands=['cancel'],
                    state=[ProductStatesGroup.title, ProductStatesGroup.addmore, ProductStatesGroup.delete, ProductStatesGroup.menu])
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await ProductStatesGroup.title.set()
    await message.answer('Вы отменили действие!',
                         reply_markup=get_start_kb_k())

@dp.message_handler(text='Посмотреть список', state=ProductStatesGroup.title)
async def kb_get_all_products(message: types.Message, state: FSMContext):
    products = await sqlite_db.get_all_products()  #
    #
    # if not products:
    #     await message.answer('Вообще продуктов нет!')

    await show_all_products(message, products)


@dp.message_handler(text='Добавить в список', state=ProductStatesGroup.title)
async def cb_add_new_product(message: types.Message) -> None:
    await message.answer('Отправь название продукта!',
                         reply_markup=get_cancel_kb())
    await ProductStatesGroup.addmore.set()


@dp.message_handler(text='Добавить ещё один продукт', state=ProductStatesGroup.title)
async def cb_add_more_new_product(message: types.Message) -> None:
    await message.answer('Отправь название продукта!',
                         reply_markup=get_cancel_kb())
    await ProductStatesGroup.addmore.set()


@dp.message_handler(text='Удалить ещё один продукт', state=ProductStatesGroup.title)
async def cb_add_new_product(message: types.Message) -> None:
    products = await sqlite_db.get_all_products()
    if len(products) == 0:
        await bot.send_message(chat_id=message.chat.id,
                               text='В списке сейчас ничего нет, может быть, ты хочешь что-то в него добавить?',
                               reply_markup=get_already_null_kb())
    else:
        await message.answer('Какой номер убрать из списка?',
                             reply_markup=get_cancel_kb())
        products = await sqlite_db.get_all_products()
        await show_all_products(message, products)
        await ProductStatesGroup.delete.set()


@dp.message_handler(text='Убрать из списка', state=ProductStatesGroup.title)
async def cb_add_new_product(message: types.Message) -> None:
    products = await sqlite_db.get_all_products()
    if len(products) == 0:
        await bot.send_message(chat_id=message.chat.id,
                               text='В списке сейчас ничего нет, может быть, ты хочешь что-то в него добавить?',
                               reply_markup=get_already_null_kb())
    else:
        await message.answer('Какой номер убрать из списка?',
                             reply_markup=get_cancel_kb())
        products = await sqlite_db.get_all_products()
        await show_all_products(message, products)
        await ProductStatesGroup.delete.set()


@dp.message_handler(state=ProductStatesGroup.delete)
async def check_number(message: types.Message, state: FSMContext):
    print(message.text)
    all_del_numbers = re.findall(r'\d+', message.text)
    mssg = []
    gsgs = []
    print(all_del_numbers)
    deleter_id = message.from_user.id
    name_of_adder = await sqlite_db.get_name_from_id(deleter_id)
    if len(all_del_numbers) != 0:
        for i in all_del_numbers:
            gsg = await sqlite_db.get_title_from_id(i)
            mssg += gsg
            print(mssg)
            await sqlite_db.delete_product(i)
            users = await sqlite_db.get_all_users()
            products = await sqlite_db.get_all_products()
            arr = '\n'.join(f"{product[0]}) <b>{product[1]}</b>" for product in products)
            if gsg.count(' ') == 0:
                morph = pymorphy2.MorphAnalyzer()
                butyavka = morph.parse(gsg)[0]
                accss = butyavka.inflect({'accs'})
                accs = accss.word
                gsgs += accs
            else:
                accs = gsg
            for user in users:
                user_idd = user[0]
                if user_idd != deleter_id:
                    time = datetime.datetime.now()
                    await bot.send_message(chat_id=user_idd,
                                           text=f'{name_of_adder} купил {accs}')
                    await bot.send_message(chat_id=user_idd,
                                           text=f'{name_of_adder} убрал {accs} из списка')
                    await bot.send_message(chat_id=user_idd,
                                           text=f'Список покупок в {time}:\n{arr}',
                                           parse_mode='HTML')
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Актуальный список:\n{arr}',
                               parse_mode='HTML')
        await message.reply('Продукты были успешно удалены!',
                            reply_markup=del_one_more_or_back_kb())
    else:
        await bot.send_message('Что-то ни одного номера не вижу в твоём сообщении, актуальный список:')
        products = await sqlite_db.get_all_products()
        await show_all_products(message, products)
    await ProductStatesGroup.title.set()


@dp.message_handler(state=ProductStatesGroup.addmore)
async def handle_title(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['title'] = message.text
    await sqlite_db.create_new_product(state)
    await message.reply('Продукт добавлен!',
                        reply_markup=add_one_more_or_back_kb())
    users = await sqlite_db.get_all_users()
    products = await sqlite_db.get_all_products()
    arr = '\n'.join(f"{product[0]}) <b>{product[1]}</b>" for product in products)
    adder_id = message.from_user.id
    name_of_adder = await sqlite_db.get_name_from_id(adder_id)
    if message.text.count(' ') == 0:
        morph = pymorphy2.MorphAnalyzer()
        butyavka = morph.parse(message.text)[0]
        accss = butyavka.inflect({'accs'})
        accs = accss.word
    else:
        accs = message.text
    for user in users:
        user_idd = user[0]
        if user_idd != adder_id:
            await bot.send_message(chat_id=user_idd,
                                   text=f'{name_of_adder} хочет {accs}')
            await bot.send_message(chat_id=user_idd,
                                   text=f'{name_of_adder} добавил {accs}')
            await bot.send_message(chat_id=user_idd,
                                   text=f'Обновлённый список покупок:\n{arr}',
                                   parse_mode='HTML')
    products = await sqlite_db.get_all_products()
    arr = '\n'.join(f"{product[0]}) <b>{product[1]}</b>" for product in products)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Актуальный список:\n{arr}',
                           parse_mode='HTML')
    await ProductStatesGroup.title.set()


@dp.message_handler(commands=['cancel'],
                    state=[ProductStatesGroup.Vtitle, ProductStatesGroup.Vaddmore, ProductStatesGroup.Vdelete, ProductStatesGroup.Vmenu])
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await ProductStatesGroup.Vtitle.set()
    await message.answer('Вы отменили действие!',
                         reply_markup=get_start_kb_v())


@dp.message_handler(text='Купить в Вельгу', state='*')
async def cmdV_start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Что хочешь сделать со списком?',
                           reply_markup=get_start_kb_v())
    await ProductStatesGroup.Vtitle.set()


@dp.message_handler(text='Вернуться в меню', state=ProductStatesGroup.Vtitle)
async def cb_add_new_product(message: types.Message, state: FSMContext) -> None:
    await message.answer('апчхи',
                         reply_markup=get_start_kb_v())


async def show_all_velgas(message: types.Message, velgas: list) -> None:
    sum = len(velgas)
    if sum > 0:
        arr = '\n'.join(f"{velga[0]}) <b>{velga[1]}</b>" for velga in velgas)
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Список для Вельги:\n{arr}',
                               parse_mode='HTML')
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='В списке сейчас пусто! Всё купил, умничка!')


@dp.message_handler(text='Посмотреть список', state=ProductStatesGroup.Vtitle)
async def kb_get_all_products(message: types.Message, state: FSMContext):
    velgas = await sqlite_db.get_all_velgas()  #
    #
    # if not velgas:
    #     await message.answer('Вообще продуктов нет!')

    await show_all_velgas(message, velgas)


@dp.message_handler(text='Добавить в список', state=ProductStatesGroup.Vtitle)
async def cb_add_new_product(message: types.Message) -> None:
    await message.answer('Отправь название продукта!',
                         reply_markup=get_cancel_kb())
    await ProductStatesGroup.Vaddmore.set()


@dp.message_handler(text='Добавить ещё один продукт', state=ProductStatesGroup.Vtitle)
async def cb_add_more_new_product(message: types.Message) -> None:
    await message.answer('Отправь название продукта!',
                         reply_markup=get_cancel_kb())
    await ProductStatesGroup.Vaddmore.set()


@dp.message_handler(text='Удалить ещё один продукт', state=ProductStatesGroup.Vtitle)
async def cb_dellmore_new_product(message: types.Message) -> None:
    velgas = await sqlite_db.get_all_velgas()
    if len(velgas) == 0:
        await bot.send_message(chat_id=message.chat.id,
                               text='В списке сейчас ничего нет, может быть, ты хочешь что-то в него добавить?',
                               reply_markup=get_already_null_kb())
    else:
        await message.answer('Какой номер убрать из списка?',
                             reply_markup=get_cancel_kb())
        velgas = await sqlite_db.get_all_velgas()
        await show_all_velgas(message, velgas)
        await ProductStatesGroup.Vdelete.set()


@dp.message_handler(text='Убрать из списка', state=ProductStatesGroup.Vtitle)
async def cb_dell_new_product(message: types.Message) -> None:
    velgas = await sqlite_db.get_all_velgas()
    if len(velgas) == 0:
        await bot.send_message(chat_id=message.chat.id,
                               text='В списке сейчас ничего нет, может быть, ты хочешь что-то в него добавить?',
                               reply_markup=get_already_null_kb())
    else:
        await message.answer('Какой номер убрать из списка?',
                             reply_markup=get_cancel_kb())
        await show_all_velgas(message, velgas)
        await ProductStatesGroup.Vdelete.set()


@dp.message_handler(state=ProductStatesGroup.Vdelete)
async def check_number(message: types.Message, state: FSMContext):
    print(message.text)
    all_del_numbers = re.findall(r'\d+', message.text)
    print(all_del_numbers)
    for i in all_del_numbers:
        await sqlite_db.delete_velga(i)
    if len(all_del_numbers) != 0:
        await message.reply('Продукты были успешно удалены!',
                            reply_markup=del_one_more_or_back_kb())
    else:
        if message.text != '/cancel':
            await bot.send_message(message.chat.id,
                                   text='Что-то ни одного номера не вижу в твоём сообщении, актуальный список:')
    velgas = await sqlite_db.get_all_velgas()
    await show_all_velgas(message, velgas)
    await ProductStatesGroup.Vtitle.set()


@dp.message_handler(state=ProductStatesGroup.Vaddmore)
async def handle_title(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    await sqlite_db.create_new_velga(state)
    await message.reply('Продукт добавлен!',
                        reply_markup=add_one_more_or_back_kb())
    await ProductStatesGroup.Vtitle.set()


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
