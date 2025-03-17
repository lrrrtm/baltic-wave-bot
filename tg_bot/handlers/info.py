from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from db.crud import get_user_cards

router = Router()


@router.message(Command("info"))
async def cmd_info(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text=f"<b>ℹ️ Информация о боте</b>"
             f"\n\nДанный бот позволяет просматривать информацию о проездных картах \"Волна Балтики\"."
             f"\n\n<b>Доступные возможности</b>"
             f"\n- хранение информации о 5 картах одновременно"
             f"\n- данные о балансе карты"
             f"\n- пополнение карты черз СБП"
             f"\n\nБот не хранит никакую информацию о пользователе за исключением номеров карт \"Волна Балтики\"."
             f"\n\nБот является неофициальным, создан и поддерживается энтузиастом для облегчения доступа населения Калининградской области к системе оплаты проезда."
             f"\n\nЕсли у вас возникли вопросы или появлилась идея для расширения функционала бота, заполните <a href=\"https://forms.yandex.ru/u/67d7feb684227c1bf80f15a7/\">эту форму</a>."
    )
