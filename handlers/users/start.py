from aiogram import F
from aiogram.filters import CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from data.config import ADMINS
from keyboards.default import admin_menu, django_menu, usat_journal_menu
from loader import dp


class AdminFilter(Filter):
    async def __call__(self, msg: Message) -> bool:
        return str(msg.from_user.id) in ADMINS


@dp.message(CommandStart(), AdminFilter())
async def bot_start(message: Message, state: FSMContext):
    await message.answer(f"Bosh sahifa", reply_markup=admin_menu)
    await state.clear()


@dp.message(AdminFilter(), F.text == "🎓 Django academy uchun")
async def django_academy_menu(msg: Message):
    await msg.answer("Django academy uchun qanday sertifikat chiqarmoqchisiz?", reply_markup=django_menu)


@dp.message(AdminFilter(), F.text == "📓 USAT journal uchun")
async def usat_journal_menu_func(msg: Message):
    await msg.answer("USAT journal uchun qanday sertifikat chiqarmoqchisiz?", reply_markup=usat_journal_menu)
