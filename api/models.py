from typing import List

from pydantic import BaseModel


class Trip(BaseModel):
    ticket_order_id: str
    route_number: str
    route_name: str
    vehicle_type_name: str
    vehicle_gov_number: str
    carrier_name: str
    total_amount_cent: int
    tickets_count: int
    fp: str | None
    date_trip: str
    date_trip_string: str
    pos_number: str


class Order(BaseModel):
    order_id: str
    amount_cent: int
    date_purchase: str
    order_type_friendly_name: str
    fp: str | None


class Card(BaseModel):
    card_id: int
    card_registration_number: str
    benefit_code: int | None
    benefit_name: str | None
    beneficiary_date_from: str | None
    beneficiary_date_to: str | None
    card_number: str
    balance_amount_cent: int
    can_be_refilled: bool
    can_buy_refills_today: bool
    can_balance_be_topped_up: bool
    refill_cost_cent: int | None
    refills: List[dict]
    periods_available_to_refill: List[dict]
    order_history: List[Order]
    tripHistory: List[Trip]
    date_expire: str
    card_release: str

class TopUpOrder(BaseModel):
    order_id: str
    url: str
    ttl_minutes: int

class TopUpStatus(BaseModel):
    order_id: str
    is_error: bool
    error: str | None
    is_finished: bool