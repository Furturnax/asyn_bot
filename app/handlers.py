from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.generators import gpt4o

router = Router()


class Generate(StatesGroup):
    text = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Привет. Задай свой вопрос.')
    await state.clear()


@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Дождитесь окончания генерации.')


@router.message(F.text)
async def generate_text(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    response = await gpt4o(message.text)
    await message.answer(response[0].message.content)
    await state.clear()
