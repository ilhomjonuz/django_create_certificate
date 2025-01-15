from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


groups_name = InlineKeyboardBuilder(
    markup=[
        [
            InlineKeyboardButton(text="🌐 Frontend", callback_data="frontend"),  # Frontend with web emoji
            InlineKeyboardButton(text="🖥️ Backend", callback_data="backend"),  # Backend with desktop computer emoji
            InlineKeyboardButton(text="🎨 Web Design", callback_data="web_design"),  # Web Design with paint palette emoji
        ]
    ]
).adjust(1, 1, 1).as_markup(resize_keyboard=True, one_time_keyboard=True)
