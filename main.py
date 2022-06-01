import sqlite3
import re
import aiogram
from sqlite3 import Cursor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

import markup as nav
from config import token

con = sqlite3.connect(r'data.db')
cur: Cursor = con.cursor()

bot = Bot(token=token)

storage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot, storage=storage)


class kbju(aiogram.dispatcher.filters.state.StatesGroup):
	calories = aiogram.dispatcher.filters.state.State()
	proteins = aiogram.dispatcher.filters.state.State()
	fats = aiogram.dispatcher.filters.state.State()
	carbohydrates = aiogram.dispatcher.filters.state.State()


class meal(aiogram.dispatcher.filters.state.StatesGroup):
	user_input = aiogram.dispatcher.filters.state.State()
	gramm_amount = aiogram.dispatcher.filters.state.State()


d = dict()
gramm = []
buttons_list = []
buttons_text = []
buttons_callbacks = []
text_list = []
calories_queries_list = []
user_id_list = []


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
	user_id = message.from_user.id
	user_id_list.append(user_id)
	name = message.from_user.first_name
	username = message.from_user.username
	cur.execute(f"""CREATE TABLE IF NOT EXISTS '{user_id}'(
			id INT PRIMARY KEY,
			name TEXT,
			username TEXT,
			calories_amount REAL,
			proteins REAL,
			fats REAL,
			carbohydrates REAL);""")
	con.commit()
	cur.execute(f"""CREATE TABLE IF NOT EXISTS '{user_id}_queries'(
				calories_query TEXT);""")
	con.commit()
	cur.execute(f"""CREATE TABLE IF NOT EXISTS '{user_id}_amounts'(
				id INT,
				calories_amount REAL,
				proteins REAL,
				fats REAL,
				carbohydrates REAL);""")

	cur.execute(f"select calories_amount from '{user_id}_amounts'")
	calories = cur.fetchone()
	first_name = message.from_user.first_name
	if calories is not None:
		cur.execute(f"select calories_amount from '{user_id}'")
		calories_user_id = cur.fetchone()
		cur.execute(f"select calories_amount from '{user_id}_amounts'")
		calories_amounts = cur.fetchone()
		if calories_amounts == calories_user_id:
			await bot.send_message(message.from_user.id, f'Привет, {first_name}👋🏻', reply_markup=nav.mainMenu)
		else:
			await bot.send_message(message.from_user.id, f'Привет, {first_name}👋🏻')
			await bot.send_message(message.from_user.id, 'Вернуть значения КБЖУ к изначальным?', reply_markup=nav.inline_kb_choice)

			@dp.callback_query_handler(lambda c: c.data and c.data == 'yes')
			async def process_callback_kb_yes(callback_query: types.CallbackQuery):
				cur.execute(f"select calories_amount from '{user_id}'")
				calories_amounts = cur.fetchone()
				cur.execute(f"select proteins from '{user_id}'")
				proteins_amounts = cur.fetchone()
				cur.execute(f"select fats from '{user_id}'")
				fats_amounts = cur.fetchone()
				cur.execute(f"select carbohydrates from '{user_id}'")
				carbohydrates_amounts = cur.fetchone()
				calories_amounts = float(*calories_amounts)
				proteins_amounts = float(*proteins_amounts)
				fats_amounts = float(*fats_amounts)
				carbohydrates_amounts = float(*carbohydrates_amounts)
				cur.execute(f"update '{user_id}_amounts' set calories_amount = '{calories_amounts}' where id = 1;")
				cur.execute(f"update '{user_id}_amounts' set proteins = '{proteins_amounts}' where id = 1;")
				cur.execute(f"update '{user_id}_amounts' set fats = '{fats_amounts}' where id = 1;")
				cur.execute(f"update '{user_id}_amounts' set carbohydrates = '{carbohydrates_amounts}' where id = 1;")
				con.commit()
				await bot.send_message(callback_query.from_user.id, "Вернул 😇", reply_markup=nav.mainMenu)

			@dp.callback_query_handler(lambda c: c.data and c.data == 'no')
			async def process_callback_kb_no(callback_query: types.CallbackQuery):
				await bot.send_message(callback_query.from_user.id, 'Понятно 😇', reply_markup=nav.mainMenu)
	else:
		await bot.send_message(message.from_user.id, f'Привет, {first_name}👋🏻', reply_markup=nav.registrationMenu)


@dp.message_handler()
async def main(message: types.Message):
	meal_number = -1
	user_id = message.from_user.id
	name = message.from_user.first_name
	username = message.from_user.username
	cur.execute(f"update '{user_id}' set name = '{name}' where id = 1;")
	cur.execute(f"update '{user_id}' set username = '{username}' where id = 1;")

	if message.text == '👤 Профиль':
		await message.delete()
		await bot.send_message(message.from_user.id, f"Имя: {name}\n"
													 f"Никнейм: @{username}")

	elif message.text == '🔐 Пройти регистрацию':
		await message.delete()
		await bot.send_message(message.from_user.id, 'Введите кол-во калорий в день: ')
		await kbju.calories.set()
		user_id = message.from_user.id
		cur.execute(f"insert into '{user_id}' (id) values('1')")
		cur.execute(f"insert into '{user_id}_amounts' (id) values('1')")

		@dp.message_handler(state=kbju.calories)
		async def enter_calories(message: types.Message, state: FSMContext):
			async with state.proxy() as data:
				data['calories'] = message.text
				calories = float(data['calories'])
				cur.execute(f"update '{user_id}_amounts' set calories_amount = '{calories}' where id = 1;")
				cur.execute(f"update '{user_id}' set calories_amount = '{calories}' where id = 1;")
				con.commit()
				await kbju.proteins.set()
				await bot.send_message(message.from_user.id, 'Введите кол-во белков в день: ')

		@dp.message_handler(state=kbju.proteins)
		async def enter_proteins(message: types.Message, state: FSMContext):
			async with state.proxy() as data:
				user_id = message.from_user.id
				data['proteins'] = message.text
				proteins = float(data['proteins'])
				cur.execute(f"update '{user_id}_amounts' set proteins = '{proteins}' where id = 1;")
				cur.execute(f"update '{user_id}' set proteins = '{proteins}' where id = 1;")
				con.commit()
				await kbju.fats.set()
				await bot.send_message(message.from_user.id, 'Введите кол-во жиров в день: ')

		@dp.message_handler(state=kbju.fats)
		async def enter_fats(message: types.Message, state: FSMContext):
			async with state.proxy() as data:
				user_id = message.from_user.id
				data['fats'] = message.text
				fats = float(data['fats'])
				cur.execute(f"update '{user_id}_amounts' set fats = '{fats}' where id = 1;")
				cur.execute(f"update '{user_id}' set fats = '{fats}' where id = 1;")
				con.commit()
				await kbju.carbohydrates.set()
				await bot.send_message(message.from_user.id, 'Введите кол-во углеводов в день: ')

		@dp.message_handler(state=kbju.carbohydrates)
		async def enter_carbohydrates(message: types.Message, state: FSMContext):
			async with state.proxy() as data:
				user_id = message.from_user.id
				data['carbohydrates'] = message.text
				carbohydrates = float(data['carbohydrates'])
				cur.execute(f"update '{user_id}_amounts' set carbohydrates = '{carbohydrates}' where id = 1;")
				cur.execute(f"update '{user_id}' set carbohydrates = '{carbohydrates}' where id = 1;")
				con.commit()

			cur.execute(f"select calories_amount from '{user_id}' where id = 1")
			calories = cur.fetchone()
			calories = float(*calories)
			cur.execute(f"select fats from '{user_id}_amounts' where id = 1")
			fats = cur.fetchone()
			fats = float(*fats)
			cur.execute(f"select proteins from '{user_id}_amounts' where id = 1")
			proteins = cur.fetchone()
			proteins = float(*proteins)
			cur.execute(f"select carbohydrates from '{user_id}_amounts' where id = 1")
			carbohydrates = cur.fetchone()
			carbohydrates = float(*carbohydrates)
			con.commit()
			await bot.send_message(message.from_user.id,
			f'Кол-во калорий в день: {calories}\n'
			f'Кол-во жиров в день: {fats}\n'
			f'Кол-во белков в день: {proteins}\n'
			f'Кол-во углеводов в день: {carbohydrates}',
			reply_markup=nav.foodMenu)
			await state.finish()

	elif message.text == '🍱 Еда':
		await bot.send_message(message.from_user.id, '🍱 Еда', reply_markup=nav.foodMenu)
		await message.delete()

	elif message.text == '🥗 Внести приём пищи':
		await message.delete()
		date = message.date
		date = str(date)[:-9]
		await bot.send_message(message.from_user.id, 'Введите название товара и кол-во грамм: ')
		await meal.user_input.set()

		@dp.message_handler(state=meal.user_input)
		async def enter_user_input(message: types.Message, state: FSMContext):
			async with state.proxy() as data:
				v = -1
				data['user_input'] = message.text
				user_input = str(data['user_input'])
				gramm_amount = re.findall(r'\d+', user_input)
				gramm_amount = int(*gramm_amount)
				user_input = re.sub(r'[^\w\s]+|[\d]+', r'', user_input).strip()
				await state.finish()
				user_input = user_input.title()
				print(user_input)
				cur.execute(f"SELECT names FROM products WHERE names LIKE '%{user_input}%';")
				con.commit()
				names = cur.fetchall()
				x = -1

				for i in range(len(names)):
					x = x + 1
					buttons_text.append(*names[x])
				x = -1

				for z in range(len(buttons_text)):
					v = v + 1
					x = x + 1
					item = buttons_text[x]
					buttons_list.append([InlineKeyboardButton(text=item, callback_data=f'btn{v}')])
					buttons_callbacks.append(i)
					d[f"btn{v}"] = f"{item}"
				keyboard_inline_buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)
				if len(d) != 0:
					await bot.send_message(message.from_user.id, 'Выберите продукт: ', reply_markup=keyboard_inline_buttons)
					pass
				else:
					await bot.send_message(message.from_user.id, 'Такого продукта нет 😕', reply_markup=nav.foodMenu)

				@dp.callback_query_handler(lambda c: c.data.startswith('btn'))
				async def process_callback_button(callback_query: types.CallbackQuery):
					await callback_query.message.edit_reply_markup()
					await bot.send_message(message.from_user.id, 'Выберите приём пищи:', reply_markup=nav.inline_kb)
					id = callback_query.data
					print(id)
					text = d[f'{id}']
					text_list.append(text)
					cur.execute(
						f"SELECT calories, proteins, fats, carbohydrates FROM products WHERE names is '{text}';")
					con.commit()
					list_all = cur.fetchall()
					calories_callback = int(list_all[0][0])
					proteins_callback = int(list_all[0][1])
					fats_callback = int(list_all[0][2])
					carbohydrates_callback = int(list_all[0][3])
					cur.execute(f"SELECT calories_amount, proteins, fats, carbohydrates "
								f"FROM '{user_id}_amounts';")
					con.commit()
					list_amounts = cur.fetchall()
					calories_amount = int(list_amounts[0][0])
					proteins_amount = int(list_amounts[0][1])
					fats_amount = int(list_amounts[0][2])
					carbohydrates_amount = int(list_amounts[0][3])
					calories_total = calories_callback * gramm_amount / 100
					proteins_total = proteins_callback * gramm_amount / 100
					fats_total = fats_callback * gramm_amount / 100
					carbohydrates_total = carbohydrates_callback * gramm_amount / 100
					cur.execute(f"update '{user_id}_amounts' set calories_amount = '{calories_amount - calories_total}' where id = 1;")
					con.commit()
					cur.execute(f"update '{user_id}_amounts' set fats = '{fats_amount - fats_total}' where id = 1;")
					con.commit()
					cur.execute(f"update '{user_id}_amounts' set proteins = '{proteins_amount - proteins_total}' where id = 1;")
					con.commit()
					cur.execute(f"update '{user_id}_amounts' set carbohydrates = '{carbohydrates_amount - carbohydrates_total}' where id = 1;")
					con.commit()


				@dp.callback_query_handler(lambda c: c.data and c.data.startswith('button'))
				async def process_callback_kb(callback_query: types.CallbackQuery):
					await callback_query.message.edit_reply_markup()
					code = callback_query.data
					txt = str(*text_list)
					print(txt)
					if code == 'buttonbreakfast':
						cur.execute(
							f"insert into '{user_id}_queries' (calories_query) values('{date} Завтрак {txt} {gramm_amount}г')")
						con.commit()
					elif code == 'buttondinner':
						cur.execute(
							f"insert into '{user_id}_queries' (calories_query) values('{date} Обед {txt} {gramm_amount}г')")
						con.commit()
					elif code == 'buttonsupper':
						cur.execute(
							f"insert into '{user_id}_queries' (calories_query) values('{date} Ужин {txt} {gramm_amount}г')")
						con.commit()
					elif code == 'buttonsnack':
						cur.execute(
							f"insert into '{user_id}_queries' (calories_query) values('{date} Перекус {txt} {gramm_amount}г')")
						con.commit()
					await bot.send_message(message.from_user.id, 'Вы успешно внесли приём пищи 😎',
					reply_markup=nav.foodMenu)

	elif message.text == '🌮 КБЖУ':
		await message.delete()
		cur.execute(f"select calories_amount from '{user_id}_amounts'")
		calories = cur.fetchone()
		cur.execute(f"select fats from '{user_id}_amounts'")
		fats = cur.fetchone()
		cur.execute(f"select proteins from '{user_id}_amounts'")
		proteins = cur.fetchone()
		cur.execute(f"select carbohydrates from '{user_id}_amounts'")
		carbohydrates = cur.fetchone()
		con.commit()
		calories = str(*calories)
		fats = str(*fats)
		proteins = str(*proteins)
		carbohydrates = str(*carbohydrates)
		await bot.send_message(message.from_user.id,
		f'Осталось калорий сегодня: {calories}\n'
		f'Осталось жиров сегодня: {fats}\n'
		f'Осталось белков сегодня: {proteins}\n'
		f'Осталось углеводов сегодня: {carbohydrates}',
		reply_markup=nav.inline_kb_edit)

	elif message.text == '💾 Мои приёмы пищи':
		await message.delete()
		cur.execute(f"select calories_query from '{user_id}_queries'")
		calories_queries = cur.fetchall()
		if len(calories_queries) == 0:
			await bot.send_message(message.from_user.id, 'У вас пока нет записей!', reply_markup=nav.foodMenu)
		else:
			for i in range(len(calories_queries)):
				meal_number = meal_number + 1
				element = str(*calories_queries[meal_number])
				await bot.send_message(message.from_user.id, f'{element}', reply_markup=nav.foodMenu)

	elif message.text == '⬅️ Назад':
		await message.delete()
		await bot.send_message(message.from_user.id, '⬅️ Назад', reply_markup=nav.mainMenu)

	elif message.text == '⬅️ Вернуться назад':
		await message.delete()
		await bot.send_message(message.from_user.id, '⬅️ Вернуться назад', reply_markup=nav.foodMenu)


@dp.callback_query_handler(lambda c: c.data and c.data == 'kbju')
async def process_callback_kbju(callback_query: types.CallbackQuery):
	await bot.send_message(callback_query.from_user.id, 'Введите кол-во калорий в день: ')
	await kbju.calories.set()
	user_id = callback_query.from_user.id

	@dp.message_handler(state=kbju.calories)
	async def enter_calories(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			data['calories'] = message.text
			calories = float(data['calories'])
			cur.execute(f"update '{user_id}_amounts' set calories_amount = '{calories}' where id = 1;")
			cur.execute(f"update '{user_id}' set calories_amount = '{calories}' where id = 1;")
			con.commit()
			await kbju.proteins.set()
			await bot.send_message(message.from_user.id, 'Введите кол-во белков в день: ')

	@dp.message_handler(state=kbju.proteins)
	async def enter_proteins(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			user_id = message.from_user.id
			data['proteins'] = message.text
			proteins = float(data['proteins'])
			cur.execute(f"update '{user_id}_amounts' set proteins = '{proteins}' where id = 1;")
			cur.execute(f"update '{user_id}' set proteins = '{proteins}' where id = 1;")
			con.commit()
			await kbju.fats.set()
			await bot.send_message(message.from_user.id, 'Введите кол-во жиров в день: ')

	@dp.message_handler(state=kbju.fats)
	async def enter_fats(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			user_id = message.from_user.id
			data['fats'] = message.text
			fats = float(data['fats'])
			cur.execute(f"update '{user_id}_amounts' set fats = '{fats}' where id = 1;")
			cur.execute(f"update '{user_id}' set fats = '{fats}' where id = 1;")
			con.commit()
			await kbju.carbohydrates.set()
			await bot.send_message(message.from_user.id, 'Введите кол-во углеводов в день: ')

	@dp.message_handler(state=kbju.carbohydrates)
	async def enter_carbohydrates(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			user_id = message.from_user.id
			data['carbohydrates'] = message.text
			carbohydrates = float(data['carbohydrates'])
			cur.execute(f"update '{user_id}_amounts' set carbohydrates = '{carbohydrates}' where id = 1;")
			cur.execute(f"update '{user_id}' set carbohydrates = '{carbohydrates}' where id = 1;")
			con.commit()

		cur.execute(f"select calories_amount from '{user_id}' where id = 1")
		calories = cur.fetchone()
		calories = float(*calories)
		cur.execute(f"select fats from '{user_id}_amounts' where id = 1")
		fats = cur.fetchone()
		fats = float(*fats)
		cur.execute(f"select proteins from '{user_id}_amounts' where id = 1")
		proteins = cur.fetchone()
		proteins = float(*proteins)
		cur.execute(f"select carbohydrates from '{user_id}_amounts' where id = 1")
		carbohydrates = cur.fetchone()
		carbohydrates = float(*carbohydrates)
		con.commit()
		await bot.send_message(message.from_user.id,
		f'Кол-во калорий в день: {calories}\n'
		f'Кол-во жиров в день: {fats}\n'
		f'Кол-во белков в день: {proteins}\n'
		f'Кол-во углеводов в день: {carbohydrates}',
		reply_markup=nav.foodMenu)
		await state.finish()

@dp.callback_query_handler(lambda c: c.data and c.data == 'kbju_back')
async def process_callback_back(callback_query: types.CallbackQuery):
	await bot.send_message(callback_query.from_user.id, 'Вы вернулись в меню 😉', reply_markup=nav.foodMenu)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
