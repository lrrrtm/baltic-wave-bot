from datetime import datetime

import requests

class VolnaCard:
    def __init__(self, card_number: int):
        self.card_number = card_number
        self.card_id = None
        self.expired_at = None
        self.last_ride = None
        self.all_card_info = None
        self.can_balance_be_topped_up = None
        self.base_url = "https://beneficiary-kd-api.icom24.ru/api"

        self._get_card_info()

    def _get_card_info(self):
        url = f"{self.base_url}/card/information?cardNumber={self.card_number}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            self.all_card_info = data
            self.card_id = data["cardId"]
            self.expired_at = datetime.strptime(data['dateExpire'], '%Y-%m-%d') if data['beneficiaryDateTo'] is None else datetime.strptime(data['beneficiaryDateTo'], '%Y-%m-%d')
            self.last_ride = data.get('tripHistory')[0] if data.get('tripHistory') else None
            self.card_balance = data['balanceAmountCent']
            self.can_balance_be_topped_up = data['canBalanceBeToppedUp']
        else:
            return None

    def get_top_up_link(self, amount_cent: int) -> dict | None:
        url = f"{self.base_url}/order/prepare/balance"
        body = {
            "cardId": self.card_id,
            "amountCent": amount_cent
        }
        response = requests.post(
            url,
            json=body
        )

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_order_status(self, order_id: str) -> dict | None:
        url = f"{self.base_url}/order/status?orderId={order_id}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None