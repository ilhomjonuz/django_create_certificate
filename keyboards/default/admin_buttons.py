from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder

admin_menu = ReplyKeyboardBuilder(
    markup=[
        [
            KeyboardButton(text="🎓 Django academy uchun")  # Graduation cap emoji for academic purposes
        ],
        [
            KeyboardButton(text="📓 USAT journal uchun")  # Notebook emoji for journal-related content
        ],
    ]
).adjust(1, 1).as_markup(resize_keyboard=True, one_time_keyboard=False)


django_menu = ReplyKeyboardBuilder(
    markup=[
        [
            KeyboardButton(text="🏆 Sertifikat olish")  # Finish-related emoji for certificate
        ],
        [
            KeyboardButton(text="💸 Vaucher olish"),  # Money-related emoji for voucher
        ],
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ]
).adjust(1, 1).as_markup(resize_keyboard=True, one_time_keyboard=True)


usat_journal_menu = ReplyKeyboardBuilder(
    markup=[
        [
            KeyboardButton(text="📄 Maqola uchun sertifikat")  # Document emoji for certificates
        ],
        [
            KeyboardButton(text="🔙 Orqaga")  # Back arrow emoji for navigation
        ]
    ]
).adjust(1, 1).as_markup(resize_keyboard=True, one_time_keyboard=True)
