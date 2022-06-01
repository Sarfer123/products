import sqlite3
from sqlite3 import Cursor
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import token

bot = Bot(token=token)

dp: Dispatcher = Dispatcher(bot)

con = sqlite3.connect(r'data.db')
cur: Cursor = con.cursor()

btn = KeyboardButton('👤 Профиль')
btn1 = KeyboardButton('🍱 Еда')
btn2 = KeyboardButton('🥗 Внести приём пищи')
btn3 = KeyboardButton('🌮 КБЖУ')
btn6 = KeyboardButton('💾 Мои приёмы пищи')
btn7 = KeyboardButton('🍕 Завтрак')
btn8 = KeyboardButton('🫕 Обед')
btn9 = KeyboardButton('🌮 Ужин')
btn10 = KeyboardButton('🍣 Перекус')
btn11 = KeyboardButton('⬅️ Назад')
btn12 = KeyboardButton('Да')
btn13 = KeyboardButton('Нет')
btn14 = KeyboardButton('🌮 Ввести количество калорий:')
btn15 = KeyboardButton('⬅️ Вернуться назад')
btn16 = KeyboardButton('🔐 Пройти регистрацию')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1, btn)
foodMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn3, btn2, btn6, btn11)
mealMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn7, btn8, btn9, btn10)
choiceMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn12, btn13)
caloriesMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn14, btn15)
registrationMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn16)

inline_btn_1 = InlineKeyboardButton('🍕 Завтрак', callback_data='buttonbreakfast')
inline_btn_2 = InlineKeyboardButton('🫕 Обед', callback_data='buttondinner')
inline_btn_3 = InlineKeyboardButton('🌮 Ужин', callback_data='buttonsupper')
inline_btn_4 = InlineKeyboardButton('🍣 Перекус', callback_data='buttonsnack')
inline_kb = InlineKeyboardMarkup(row_width=2).add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4)

inline_edit = InlineKeyboardButton('Изменить КБЖУ', callback_data='kbju')
inline_back = InlineKeyboardButton('◀️ Назад', callback_data='kbju_back')
inline_kb_edit = InlineKeyboardMarkup().add(inline_edit, inline_back)

inline_choice = InlineKeyboardButton('Да', callback_data='yes')
inline_choice_1 = InlineKeyboardButton('Нет', callback_data='no')
inline_kb_choice = InlineKeyboardMarkup(row_width=2).add(inline_choice, inline_choice_1)