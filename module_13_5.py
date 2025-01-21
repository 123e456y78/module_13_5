import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter, CommandStart
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from reply import get_keyboard
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
api = '7314899914:AAHcsc1SyUJccc3bK3jNxYvAkCdAfC8fxas'
bot = Bot(token=api)
dp = Dispatcher()
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.',
                         reply_markup=get_keyboard('Рассчитать', 'Информация',
                                                   placeholder="Выберите нужное действие",
                                                   sizes=(2, 0)),
                         )
    print('Привет! Я бот, помогающий твоему здоровью.')
class UserState(StatesGroup):
    age = State()  # Возраст
    growth = State()  # Рост
    weight = State()  # Вес
@dp.message(StateFilter(None),F.text == 'Рассчитать')
async def set_age(message: types.Message, state: FSMContext):
    await message.answer('Введите свой возраст:', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserState.age)
@dp.message(UserState.age, F.text)
async def set_growth(message: types.Message, state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await message.answer('Вы ввели неправильно, введите возраст еще раз:')
        return
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await state.set_state(UserState.growth)
@dp.message(UserState.growth, F.text)
async def set_weight(message: types.Message, state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await message.answer('Вы ввели данные неправильно, введите рост в см еще раз:')
        return
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await state.set_state(UserState.weight)
@dp.message(UserState.weight, F.text)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    try:
        int(message.text)
    except ValueError:
        await message.answer('Вы ввели данные о весе неправильно, введите вес в кг еще раз:')
        return
    data = await state.get_data()
    print(data)
    norm_calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    print(norm_calories)
    await message.answer(str(f'Ваша норма калорий: {norm_calories}'))
    await state.clear()
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())