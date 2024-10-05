from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

import crud_functions

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Купить')],
        [KeyboardButton(text='Регистрация')],
    ], resize_keyboard=True)


kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.add(button)
kb.add(button2)


@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=start_menu)


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    await message.answer(f'Название: {crud_functions.get_all_products1()[0][0]} | '
                         f'Описание: {crud_functions.get_all_products1()[0][1]}  | '
                         f'Цена: {crud_functions.get_all_products1()[0][2]}')
    with open(f'{crud_functions.get_all_products1()[0][3]}', 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo)

    await message.answer(f'Название: {crud_functions.get_all_products2()[0][0]} | '
                         f'Описание: {crud_functions.get_all_products2()[0][1]}  | '
                         f'Цена: {crud_functions.get_all_products2()[0][2]}')
    with open(f'{crud_functions.get_all_products2()[0][3]}', 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo)

    await message.answer(f'Название: {crud_functions.get_all_products3()[0][0]} | '
                         f'Описание: {crud_functions.get_all_products3()[0][1]}  | '
                         f'Цена: {crud_functions.get_all_products3()[0][2]}')
    with open(f'{crud_functions.get_all_products3()[0][3]}', 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo)

    await message.answer(f'Название: {crud_functions.get_all_products4()[0][0]} | '
                         f'Описание: {crud_functions.get_all_products4()[0][1]}  | '
                         f'Цена: {crud_functions.get_all_products4()[0][2]}')
    with open(f'{crud_functions.get_all_products4()[0][3]}', 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo)


@dp.callback_query_handler(lambda call: call.data.startswith('buy_'))
async def handle_purchase(call: types.CallbackQuery):
    product_code = call.data.split('_')[1]

    product_names = {
        'Analgin': 'Анальгин',
        'Vitamin B12': 'Витамин В12',
        'Ibuprofen': 'Ибупрофен',
        'Festal': 'Фестал'
    }

    product_name = product_names.get(product_code, 'Продукт')

    await call.message.answer(f'Вы успешно приобрели {product_name}!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer(
        'Формула расчёта калорий:\n10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161'
    )
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост (в см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес (в кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    weight = data['weight']
    growth = data['growth']
    age = data['age']

    result = (10 * weight) + (6.25 * growth) - (5 * age) - 161
    await message.answer(f'Ваша норма калорий: {result:.2f} ккал в день.')
    await state.finish()


@dp.message_handler(text='Информация')
async def inform(message: types.Message):
    await message.answer('Информация о боте!', reply_markup=start_menu)


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer(text='Выберите опцию:', reply_markup=kb)


@dp.message_handler(text='Регистрация')
async def sing_up(message: types.Message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    if not re.match("^[A-Za-z]+$", message.text):
        await message.answer('Имя пользователя должно содержать только латинские буквы. Попробуйте снова.')
        return

    if not crud_functions.is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()

    if crud_functions.is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя')
        await message.answer('Введите имя пользователя (только латинский алфавит):')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Регистрация завершена! Ваш баланс будет пополнен на 1000.')

    await state.update_data(balance=1000)

    data = await state.get_data()
    username = data['username']
    email = data['email']
    age = data['age']
    balance = data['balance']

    crud_functions.add_user(username=username, email=email, age=age, balance=balance)

    await message.answer(f'Пользователь {username} успешно зарегистрирован!')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
