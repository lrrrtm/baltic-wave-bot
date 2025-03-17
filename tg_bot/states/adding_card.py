from aiogram.fsm.state import StatesGroup, State


class AddingCardMessage(StatesGroup):
    waiting_for_msg = State()
    card_number = State()
    card_name = State()

class AddingCardNameMessage(StatesGroup):
    waiting_for_msg = State()