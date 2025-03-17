import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import FSInputFile

from tg_bot.db.crud import get_user_cards, add_new_card
from tg_bot.handlers.my_cards import cmd_my_cards
from tg_bot.keyboards.callback_factories import AddCardCF
from tg_bot.states.adding_card import AddingCardMessage, AddingCardNameMessage
from utils.volna_api import VolnaCard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    user_cards = get_user_cards(telegram_id=message.from_user.id)
    if user_cards:
        await cmd_my_cards(message, state)
    else:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="🆕 Добавить карту",
            callback_data=AddCardCF(telegram_id=message.from_user.id)
        )
        await message.answer(
            text=f"👋 Приветствуем вас в боте «Волна Балтики»!"
                 f"\n\n👀 С помощью него можно с удобством просматривать информацию о проездных картах, а также пополнять их через СБП."
                 f"\n\nℹ️ Более подробная информация: /info"
                 f"\n\n🚎 Чтобы начать, необходимо добавить хотя бы одну карту. Чтобы это сделать, нажмите на кнопку под сообщением",
            reply_markup=builder.as_markup()
        )


@router.callback_query((AddCardCF.filter()))
async def add_card(callback: CallbackQuery, callback_data: AddCardCF, state: FSMContext):
    await state.clear()

    await callback.message.delete()

    user_cards = get_user_cards(telegram_id=callback_data.telegram_id)
    if len(user_cards) < 5:

        builder = ReplyKeyboardBuilder()
        builder.button(
            text="❌ Отменить"
        )

        await callback.message.answer_photo(
            photo=FSInputFile(os.path.join(os.getenv('ROOT_FOLDER'), 'static_data', 'images', 'card_back_number.png')),
            caption="<b>🆕 Добавление карты</b>"
                    "\n\n#️⃣ Отправьте номер транспортной карты. Он расположен на обратной стороне карты под штрих-кодом",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(AddingCardMessage.waiting_for_msg)
    else:
        await callback.message.answer(
            text="<b>🆕 Добавление карты</b>"
                 "\n\n🔴 К вашему аккаунту привязано максимальное количество карт (5). Чтобы добавить новую карту, удалите одну из существующих"
        )


@router.message(AddingCardMessage.waiting_for_msg)
async def add_card_process(message: Message, state: FSMContext):
    await state.clear()

    input_card_number = message.text.strip()

    if input_card_number == "❌ Отменить":
        await message.answer(
            text="❌ Действие отменено",
            reply_markup=ReplyKeyboardRemove()
        )
        await cmd_start(message, state)

    elif input_card_number.isdigit():
        volna = VolnaCard(card_number=int(input_card_number))
        if volna.all_card_info is not None:

            user_cards = [card.card_number for card in get_user_cards(telegram_id=message.from_user.id)]

            if input_card_number not in user_cards:

                await state.update_data({'card_number': input_card_number})

                builder = ReplyKeyboardBuilder()
                builder.button(
                    text="🫥 Оставить без названия"
                )

                await message.answer(
                    text=f"<b>🆕 Добавление карты</b>"
                         f"\n\nВведите название для карты (например: «Карта Вани» или «Мамина»), чтобы её было удобно искать в списке карт."
                         f"\n\nЕсли название не требуется, нажмите на «🫥 Оставить без названия»",
                    reply_markup=builder.as_markup(resize_keyboard=True)
                )

                await state.set_state(AddingCardMessage.card_name)
            else:
                await message.answer(
                    text="😎 Данная карта <b>уже привязана</b> к вашему аккаунту, введите номер другой карты или отмените добавление, нажав кнопку на клавиуатуре"
                )
                await state.set_state(AddingCardMessage.waiting_for_msg)
        else:
            await message.answer(
                text="😰 Карта с таким номером <b>не найдена</b>, проверьте правильность отправленного номера карты и попробоуйте ещё раз"
            )
            await state.set_state(AddingCardMessage.waiting_for_msg)
    else:
        await message.answer(
            text="😰 Карта с таким номером <b>не найдена</b>, проверьте правильность отправленного номера карты и попробоуйте ещё раз"
        )
        await state.set_state(AddingCardMessage.waiting_for_msg)


@router.message(AddingCardMessage.card_name)
async def add_card_name_process(message: Message, state: FSMContext):
    card_number = await state.get_value('card_number')

    card_name = message.text.strip() if message.text.strip() != '🫥 Оставить без названия' else str(card_number)


    add_new_card(card_number=int(card_number), card_name=card_name, telegram_id=message.from_user.id)

    if card_name == str(card_number):
        text = ''
    else:
        text = f" «{card_name}»"

    await message.answer(
        text=f"<b>🆕 Добавление карты</b>"
             f"\n\n🎉 Карта <b>{card_number}{text}</b> успешно добавлена! Перейдите в /cards, чтобы посмотреть",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()
