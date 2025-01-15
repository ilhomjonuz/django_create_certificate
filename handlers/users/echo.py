from aiogram import types, F
from aiogram.fsm.state import State

from keyboards.default import admin_menu
from loader import dp


@dp.message(State(), F.text == "🔙 Orqaga")
async def bad_message(message: types.Message):
    await message.answer("Bosh sahifa", reply_markup=admin_menu)

# Echo bot
@dp.message(State())
async def bot_echo(message: types.Message):
    await message.answer(message.text)


@dp.callback_query(State())
async def bad_callback_query(call: types.CallbackQuery):
    await call.message.edit_text("Xabar o'chirildi.")
