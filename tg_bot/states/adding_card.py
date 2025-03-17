from aiogram.fsm.state import StatesGroup, State


class AddingCardMessage(StatesGroup):
    waiting_for_msg = State()