from aiogram.fsm.state import StatesGroup, State


class ArticleStates(StatesGroup):
    fullname = State()
    article = State()
    issue = State()
    year = State()
    date = State()
