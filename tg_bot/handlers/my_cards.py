from typing import List

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.db.crud import get_user_cards
from tg_bot.db.models import Card
from tg_bot.keyboards.callback_factories import CardListCF, AddCardCF, CardInfoCF
from utils.volna_api import VolnaCard

router = Router()


async def get_cards_menu(user_cards: List[Card], telegram_id: int):
    builder = InlineKeyboardBuilder()

    if user_cards:
        for card in user_cards:
            builder.button(
                text=f"{card.card_number}",
                callback_data=CardListCF(card_number=card.card_number, card_id=card.id)
            )
        builder.button(
            text="🆕 Добавить карту",
            callback_data=AddCardCF(telegram_id=telegram_id)
        )

        builder.adjust(1)

        text = "<b>🪪 Мои карты</b>\n\nВыберите карту из списка"
    else:
        builder.button(
            text="🆕 Добавить карту",
            callback_data=AddCardCF(telegram_id=telegram_id)
        )
        text = "<b>🪪 Мои карты</b>\n\n🫥 У вас нет сохранённых карт. Чтобы добавить карту, нажмите на кнопку под сообщением"

    return {'text': text, 'markup': builder.as_markup()}


@router.message(Command("cards"))
async def cmd_my_cards(message, state: FSMContext):
    await state.clear()
    user_cards = get_user_cards(telegram_id=message.from_user.id)
    data = await get_cards_menu(user_cards, message.from_user.id)

    if type(message) == CallbackQuery:
        await message.message.answer(
            text=data['text'],
            reply_markup=data['markup']
        )
    else:
        await message.answer(
            text=data['text'],
            reply_markup=data['markup']
        )


@router.callback_query((CardListCF.filter()))
async def admin_menu_back_process(callback: CallbackQuery, callback_data: CardListCF, state: FSMContext):

    card_number = callback_data.card_number
    volna = VolnaCard(card_number=card_number)

    if volna.all_card_info is not None:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="💸 Пополнить баланс",
            callback_data=CardInfoCF(
                action="top_up",
                card_number=card_number,
                card_id=volna.card_id
            )
        )

        builder.button(
            text="🗑️ Удалить карту",
            callback_data=CardInfoCF(
                action="remove_card",
                card_number=card_number,
                card_id=volna.card_id
            )
        )

        builder.button(
            text="⬅️ Назад",
            callback_data=CardInfoCF(
                action="back",
                card_number=card_number,
                card_id=volna.card_id
            )
        )

        builder.adjust(1)

        if volna.last_ride:
            last_ride_text = f"\n\n🚌 Последняя поездка\n<b>{volna.last_ride['dateTripString']} {volna.last_ride['vehicleTypeName']} №{volna.last_ride['routeNumber']} ({volna.last_ride['vehicleGovNumber'].upper()})</b>"
        else:
            last_ride_text = ""
        await callback.message.edit_text(
            text=f"<b>🪪 Информация о карте</b>"
                 f"\n\n<pre>{card_number}</pre>"
                 f"\n\n💰 Текущий баланс: <b>{volna.card_balance // 100}₽</b>"
                 f"\n🗓️ Годна до: <b>{volna.expired_at.strftime('%d.%m.%Y')}</b>"
                 f"{last_ride_text}"
        )
        await callback.message.edit_reply_markup(
            reply_markup=builder.as_markup()
        )
    else:
        await callback.answer(
            text="Не удалось получить информацию о карте, попробуйте позже.",
            show_alert=True
        )