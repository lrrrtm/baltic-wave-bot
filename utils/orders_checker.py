import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import time
from datetime import datetime

import telebot

from tg_bot.db.crud import get_active_orders, update_order_status
from utils.volna_api import VolnaCard

bot = telebot.TeleBot(token=os.getenv("BOT_API_TOKEN"), parse_mode='HTML')

logging.basicConfig(level=logging.DEBUG)


def active_orders_status():
    while True:
        orders = get_active_orders()

        print(f"ACTIVE ORDERS: {len(orders)}")

        for order in orders:
            volna = VolnaCard(card_number=int(order.card_number))

            data = volna.get_order_status(order_id=order.api_uuid)
            print(f"ORDER: {order}\nSTATUS: {data}")
            if data is not None:
                is_error = bool(data['isError'])
                error_text = data['error']
                is_finished = bool(data['isFinished'])

                if is_finished:
                    update_order_status(id=order.id, order_status="success")
                    bot.send_message(
                        chat_id=order.user_tid,
                        text=f"<b>💸 Пополнение баланса</b>"
                             f"\n\nБаланс карты <b>{order.card_number}</b> успешно пополнен на <b>{order.amount}₽</b>"
                             f"\nТекущий баланс: <b>{volna.card_balance // 100}₽</b>"
                             f"\n\n🚌 Приятных поездок!"
                    )

                elif is_error:
                    bot.send_message(
                        chat_id=order.user_tid,
                        text=f"<b>💸 Пополнение баланса</b>"
                             f"\n\nПри пополнении баланса карты произошла ошибка: {error_text}."
                    )

                elif not is_finished and (datetime.now() - order.created_at).seconds > 600:
                    update_order_status(id=order.id, order_status="cancelled")

        time.sleep(5)


if __name__ == "__main__":
    active_orders_status()
