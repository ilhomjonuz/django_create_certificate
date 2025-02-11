import asyncio

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from handlers.users.start import AdminFilter
from keyboards.default import admin_menu
from loader import dp
from states import ArticleStates
from utils import generate_article_certificate


@dp.message(AdminFilter(), F.text == "📄 Maqola uchun sertifikat")
async def article_certificate(msg: Message, state: FSMContext):
    await msg.answer(f'Ushbu funksiya <a href="https://t.me/usat_journal_bot">USAT journal bot</a> boti orqali ishlaydi!')
    return
    # await msg.answer("Sertifikat oluvchining ism-familiyasini yuboring:", reply_markup=ReplyKeyboardRemove())
    # await state.set_state(ArticleStates.fullname)


@dp.message(ArticleStates.fullname, F.text)
async def get_certificate_user(msg: Message, state: FSMContext):
    await state.update_data({'fullname': msg.text})
    await msg.answer("Maqola nomini yuboring:")
    await state.set_state(ArticleStates.article)


@dp.message(ArticleStates.article, F.text)
async def get_certificate_user(msg: Message, state: FSMContext):
    await state.update_data({'article': msg.text})
    await msg.answer("Jurnal soni(issue)ni yuboring(Misol uchun: 1):")
    await state.set_state(ArticleStates.issue)


@dp.message(ArticleStates.issue, F.text.regexp(r"^\d+$"))
async def get_certificate_user(msg: Message, state: FSMContext):
    await state.update_data({'issue': msg.text})
    await msg.answer("Jurnal jildi(volume)ni yuboring(Misol uchun: 1):")
    await state.set_state(ArticleStates.volume)


@dp.message(ArticleStates.volume, F.text.regexp(r"^\d+$"))
async def get_certificate_user(msg: Message, state: FSMContext):
    await state.update_data({'volume': msg.text})
    await msg.answer("Jurnal yilini yuboring(Misol uchun: 2025):")
    await state.set_state(ArticleStates.year)


@dp.message(ArticleStates.year, F.text.regexp(r"^\d{4}$"))
async def get_certificate_user(msg: Message, state: FSMContext):
    await state.update_data({'year': msg.text})
    await msg.answer("Sertifikat berilish sanasini yuboring(Misol uchun: 01.01.2025):")
    await state.set_state(ArticleStates.date)


@dp.message(ArticleStates.date, F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})$"))
async def get_certificate_user(msg: Message, state: FSMContext):
    await state.update_data({'date': msg.text})
    data = await state.get_data()
    await state.clear()
    cert_resp = await generate_article_certificate(**data)
    if cert_resp['ok']:
        await msg.answer("⏳ Sertifikat tayyorlanmoqda...", reply_markup=admin_menu)
        cert_image = FSInputFile(cert_resp['result'])
        await msg.answer_document(cert_image)
    else:
        await msg.answer(cert_resp['result'], reply_markup=admin_menu)


@dp.message(StateFilter(ArticleStates))
async def error_choice_group(message: Message):
    await message.delete()
    warning_msg = await message.answer("❌ Iltimos, ma'lumotni to'g'ri yuboring!")
    await asyncio.sleep(3)
    await warning_msg.delete()
