from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.db.crud import get_user_cards, insert_order, remove_user_card
from tg_bot.handlers.my_cards import cmd_my_cards, get_cards_menu
from tg_bot.keyboards.callback_factories import CardInfoCF, CardTopUpCF
from utils.volna_api import VolnaCard

router = Router()


@router.callback_query((CardInfoCF.filter()))
async def card_actions(callback: CallbackQuery, callback_data: CardInfoCF, state: FSMContext):
    action = callback_data.action

    if action == 'back':
        await callback.answer()
        user_cards = get_user_cards(callback.from_user.id)

        data = await get_cards_menu(user_cards, callback.from_user.id)

        await callback.message.edit_text(
            text=data['text']
        )
        await callback.message.edit_reply_markup(
            reply_markup=data['markup']
        )

    elif action == 'top_up':
        volna = VolnaCard(card_number=callback_data.card_number)

        if volna.can_balance_be_topped_up:
            await callback.answer()
            builder = InlineKeyboardBuilder()

            for sum in [1, 100, 200, 350, 500, 1000]:
                builder.button(
                    text=f"{sum}₽",
                    callback_data=CardTopUpCF(
                        action=f"top_{sum}",
                        card_number=callback_data.card_number,
                        card_id=callback_data.card_id
                    )
                )

            builder.button(
                text="⬅️ Назад",
                callback_data=CardTopUpCF(
                    action="back",
                    card_number=callback_data.card_number,
                    card_id=callback_data.card_id
                )
            )

            builder.adjust(3)

            await callback.message.edit_text(
                text=f"<b>💸 Пополнение баланса</b>"
                     f"\n\n<pre>{callback_data.card_number}</pre>"
                     f"\n\nВыберите сумму, на которую хотите пополнить баланс карты"
            )

            await callback.message.edit_reply_markup(
                reply_markup=builder.as_markup()
            )

        else:
            await callback.answer(
                text=f"Невозможно пополнить карту {volna.card_number}",
                show_alert=True
            )

    elif action == 'remove_card':
        remove_user_card(card_number=callback_data.card_number, telegram_id=callback.from_user.id)
        await callback.answer(
            text=f"Карта {callback_data.card_number} успешно удалена!",
            show_alert=True
        )
        await callback.message.delete()
        await cmd_my_cards(callback, state)


@router.callback_query((CardTopUpCF.filter()))
async def pay_actions(callback: CallbackQuery, callback_data: CardTopUpCF, state: FSMContext):
    action = callback_data.action

    if action == 'back':
        pass

    elif action.startswith("top_"):
        amount = int(action.split("_")[-1])

        volna = VolnaCard(card_number=callback_data.card_number)
        sbp_data = volna.get_top_up_link(amount_cent=amount * 100)

        if sbp_data is not None:
            await callback.answer()
            await callback.message.edit_text(
                text=f"<b>💸 Пополнение баланса</b>"
                     f"\n\n<pre>{callback_data.card_number}</pre>"
                     f"\n\nДля пополнения баланса карты на {amount}₽ нажмите на кнопку под сообщением",
            )
            await callback.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="Оплатить через СБП", url=sbp_data['url'])]]
                )
            )

            insert_order(
                api_uuid=sbp_data['orderId'],
                amount=amount,
                url=sbp_data['url'],
                user_tid=callback.from_user.id,
                card_number=callback_data.card_number,
            )

        else:
            await callback.answer(
                text="Возникла ошибка при работе с СБП, повторите попытку позже.",
                show_alert=True
            )
