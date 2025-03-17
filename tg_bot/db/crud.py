from typing import List
from contextlib import contextmanager

from tg_bot.db.models import Card, Order
from tg_bot.db.database import Session


@contextmanager
def get_session():
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def add_new_card(card_number: int, telegram_id: int) -> Card:
    with get_session() as session:
        card = Card(telegram_id=telegram_id, card_number=str(card_number))
        session.add(card)
        session.commit()
        return card


def remove_user_card(card_number: int, telegram_id: int):
    with get_session() as session:
        session.query(Card).filter(Card.telegram_id == telegram_id, Card.card_number == str(card_number)).delete(
            synchronize_session=False)


def get_user_cards(telegram_id: int) -> List[Card]:
    with get_session() as session:
        data = session.query(Card).filter(Card.telegram_id == telegram_id).all()
        return data


def insert_order(api_uuid: str, amount: int, url: str, user_tid: int, card_number: int) -> Order:
    with get_session() as session:
        order = Order(
            api_uuid=api_uuid,
            url=url,
            amount=amount,
            user_tid=user_tid,
            card_number=str(card_number)

        )
        session.add(order)
        session.commit()
        return order


def update_order_status(id: int, order_status: str):
    with get_session() as session:
        order = session.query(Order).filter(Order.id == id).first()
        order.status = order_status
        session.commit()


def get_active_orders() -> List[Order]:
    with get_session() as session:
        data = session.query(Order).filter(Order.status == 'active').all()
        return data


if __name__ == "__main__":
    add_new_card(card_number=215050004534, telegram_id=409801981)
    # remove_user_card(card_number=215050004534, telegram_id=409801981)
    # data = get_user_cards(telegram_id=409801981)
    # for el in data:
    #     print(el.card_number)
