from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

products_cb = CallbackData('product', 'id', 'action')

def get_products_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Просмотр всех продуктов', callback_data='get_all_products')],
        [InlineKeyboardButton('Добавить новый продукт', callback_data='add_new_product')],
    ])

    return ikb


def get_edit_ikb(product_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Редактировать продукт', callback_data=products_cb.new(product_id, 'edit'))],
        [InlineKeyboardButton('Удалить продукт', callback_data=products_cb.new(product_id, 'delete'))],
    ])

    return ikb


def ikb_velga(product_id: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Список в Вельгу', callback_data=products_cb.new(product_id, 'edit'))],
        [InlineKeyboardButton('Удалить продукт', callback_data=products_cb.new(product_id, 'delete'))],
    ])

    return ikb

def get_start_kb_v() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Посмотреть список'), KeyboardButton('Добавить в список')], [KeyboardButton('Убрать из списка')]
    ], resize_keyboard=True)

    return kb


def get_already_null_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Добавить в список'), KeyboardButton('Вернуться в меню')]], resize_keyboard=True)

    return kb


def get_start_kb_k() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Посмотреть список'), KeyboardButton('Добавить в список')], [KeyboardButton('Убрать из списка')]
    ], resize_keyboard=True)

    return kb

def add_one_more_or_back_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Добавить ещё один продукт'), KeyboardButton('Вернуться в меню')]
    ], resize_keyboard=True)

    return kb


def del_one_more_or_back_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Удалить ещё один продукт'), KeyboardButton('Вернуться в меню')]
    ], resize_keyboard=True)

    return kb


def get_list_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Купить в квартиру'), KeyboardButton('Купить в Вельгу')]
    ], resize_keyboard=True)

    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('/cancel')]
    ], resize_keyboard=True)

    return kb