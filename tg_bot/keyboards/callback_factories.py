from aiogram.filters.callback_data import CallbackData


class CardListCF(CallbackData, prefix="cards_list"):
    card_number: int
    card_id: int


class AddCardCF(CallbackData, prefix="add_card"):
    telegram_id: int


class CardInfoCF(CallbackData, prefix="card_info"):
    action: str
    card_number: int
    card_id: int

class CardTopUpCF(CallbackData, prefix="card_top_up"):
    action: str
    card_number: int
    card_id: int

class StartCF(CallbackData, prefix="start"):
    action: str