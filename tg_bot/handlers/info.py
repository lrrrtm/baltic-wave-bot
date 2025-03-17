from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(Command("info"))
async def cmd_info(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text=f"<b>ℹ️ Информация о боте</b>"
             f"\n\nДанный бот позволяет просматривать информацию о проездных картах «Волна Балтики»."
             f"\n\n<b>📋 Доступные возможности</b>"
             f"\n- хранение информации о 5 картах одновременно"
             f"\n- данные о балансе карты, сроке действия и совершённых поездках"
             f"\n- пополнение баланса карты черз СБП"
             f"\n\n🚫 Бот <b>не хранит никакую информацию о пользователе</b> за исключением номеров карт «Волна Балтики»."
             f"\n\n🫂 Бот <b>является неофициальным</b>, создан и поддерживается энтузиастами для облегчения доступа населения Калининградской области к системе оплаты проезда."
             f"\n\n💬 Если у вас возникли вопросы или появилась идея для расширения функционала бота, заполните <a href=\"https://forms.yandex.ru/u/67d7feb684227c1bf80f15a7/\">эту форму</a>."
    )
