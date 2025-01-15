import asyncio

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery

from keyboards.default import admin_menu
from keyboards.inline import groups_name
from loader import dp, bot, db
from utils import create_voucher_file, create_certificate


@dp.message(lambda msg: msg.text == "💸 Vaucher olish")
async def get_voucher(msg: Message, state: FSMContext):
    # Admindan muddatni so'rash
    await msg.answer("Vaucher amal qilish muddatini kiriting:\n(Misol uchun: 01.01.2026)", reply_markup=ReplyKeyboardRemove())
    await state.set_state("get_voucher_date")


@dp.message(StateFilter("get_voucher_date"), F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})$"))
async def get_voucher_date(msg: Message, state: FSMContext):
    await msg.answer("⏳ Vaucher tayyorlanmoqda...")
    await msg.answer("Bosh sahifa", reply_markup=admin_menu)
    await state.clear()
    expiration_date = msg.text
    voucher_file = await create_voucher_file(expiration_date)
    photo = FSInputFile(voucher_file)
    await bot.send_document(chat_id=msg.chat.id, document=photo)


@dp.message(StateFilter('get_voucher_date'))
async def error_voucher_date(message: Message):
    await message.delete()
    warning_msg = await message.answer("❌ Amal qilish muddati xato.\n\nIltimos, qayta kiriting!")
    await asyncio.sleep(3)
    await warning_msg.delete()


# ----------- Create certificate ------------------------------------------------------------------------------

@dp.message(lambda msg: msg.text == "🏆 Sertifikat olish")
async def get_certificate(message: Message, state: FSMContext):
    await message.answer("Sertifikat oluvchining ism-familiyasini yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state("get_certificate_user")


@dp.message(StateFilter("get_certificate_user"), lambda msg: msg.text)
async def get_certificate_user(msg: Message, state: FSMContext):
    await state.set_data({'fullname': msg.text})
    await msg.answer("O'quv kursi yo'nalishini tanlang:", reply_markup=groups_name)
    await state.set_state("get_group_name")


COURSES = {
    'frontend': "FRONTEND DEVELOPER",
    'backend': "BACKEND DEVELOPER",
    'web_design': "GRAPHIC DESIGN",
}


@dp.callback_query(StateFilter("get_group_name"), lambda call: call.data)
async def get_group_name(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.edit_text("⏳ Sertifikat tayyorlanmoqda...")
    await call.message.answer("Bosh sahifa", reply_markup=admin_menu)
    await state.clear()
    fullname = data.get('fullname')
    course = COURSES.get(call.data)
    cert_id = await db.add_certificate(fullname, course)
    response = await create_certificate(cert_id, fullname, course)

    if response['status'] == 'ok':
        await db.update_cert_image(cert_id, response['result'][6:])
        await call.message.answer_document(FSInputFile(response['result']))
    else:
        await call.message.answer(response['result'])


@dp.message(StateFilter("get_group_name"))
async def error_choice_group(message: Message):
    await message.delete()
    warning_msg = await message.answer("❌ Iltimos, yuqoridagi tugmnalardan foydalanib o'quv kursi yo'nalishini tanlang!")
    await asyncio.sleep(3)
    await warning_msg.delete()
