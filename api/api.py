import requests

from models import Card, Trip, Order, TopUpOrder, TopUpStatus
from pydantic import BaseModel
from requests import get, post, RequestException


class RequestResponse(BaseModel):
    ok: bool
    error: str | None
    data: Card | TopUpOrder | TopUpStatus | None


class API:
    def __init__(self):
        self.base_url = "https://beneficiary-kd-api.icom24.ru/api"

    def _make_request(self, url: str, method: str = "POST", body: dict = None, timeout: int = 5):
        if method == "POST":
            error = ""
            response = None
            try:
                response = post(
                    url=url,
                    json=body,
                    timeout=timeout
                )
            except requests.exceptions.Timeout:
                error = "Превышено время ожидания запроса"
            except requests.exceptions.ConnectionError:
                error = "Ошибка подключения к серверу"
            except requests.exceptions.HTTPError as err:
                error = f"HTTP-ошибка: {err}"
            except requests.exceptions.RequestException as err:
                error = f"Произошла ошибка при выполнении запроса: {err}"
            except requests.exceptions.JSONDecodeError:
                error = "Ошибка при декодировании JSON-ответа"
            finally:
                return response, error

    def get_order_status(self, order_id: str) -> RequestResponse:
        url = f"{self.base_url}/order/status?orderId={order_id}"

        ok = False
        error = None

        try:
            response = get(
                url=url,
                timeout=5
            )

            data = response.json()
            if data.get("status") and data.get("title"):
                error = f"[{data['status']}] {data['title']}"
            else:
                ok = True
                error = None

        except requests.exceptions.Timeout:
            error = "Превышено время ожидания запроса"
        except requests.exceptions.ConnectionError:
            error = "Ошибка подключения к серверу"
        except requests.exceptions.HTTPError as err:
            error = f"HTTP-ошибка: {err}"
        except requests.exceptions.RequestException as err:
            error = f"Произошла ошибка при выполнении запроса: {err}"
        except requests.exceptions.JSONDecodeError:
            error = "Ошибка при декодировании JSON-ответа"
        finally:
            if ok:
                return RequestResponse(
                    ok=ok,
                    error=error,
                    data=TopUpStatus(
                        order_id=order_id,
                        is_error=bool(data.get("isError")),
                        error=data.get("error"),
                        is_finished=bool(data.get("isFinished"))
                    )
                )
            else:
                return RequestResponse(
                    ok=ok,
                    error=error,
                    data=None
                )

    def get_top_up_link(self, card_id: int, amount_cent: int) -> RequestResponse:
        url = f"{self.base_url}/order/prepare/balance"

        ok = False
        error = None

        try:
            response = post(
                url=url,
                json={
                    "cardId": card_id,
                    "amountCent": amount_cent
                },
                timeout=5
            )

            data = response.json()
            if data.get("status") and data.get("title"):
                error = f"[{data['status']}] {data['title']}"
            else:
                ok = True
                error = None

        except requests.exceptions.Timeout:
            error = "Превышено время ожидания запроса"
        except requests.exceptions.ConnectionError:
            error = "Ошибка подключения к серверу"
        except requests.exceptions.HTTPError as err:
            error = f"HTTP-ошибка: {err}"
        except requests.exceptions.RequestException as err:
            error = f"Произошла ошибка при выполнении запроса: {err}"
        except requests.exceptions.JSONDecodeError:
            error = "Ошибка при декодировании JSON-ответа"
        finally:
            if ok:
                return RequestResponse(
                    ok=ok,
                    error=error,
                    data=TopUpOrder(
                        order_id=data.get("orderId"),
                        url=data.get("url"),
                        ttl_minutes=data.get("ttlMinutes"),
                    )
                )
            else:
                return RequestResponse(
                    ok=ok,
                    error=error,
                    data=None
                )

    def card_check(self, card_number: int) -> RequestResponse:
        url = f"{self.base_url}/card/check/"

        ok = False
        error = None

        try:
            response = post(
                url=url,
                json={
                    "cardNumber": f"{card_number}"
                },
                timeout=5
            )

            data = response.json()
            if data.get("status") and data.get("title"):
                error = f"[{data['status']}] {data['title']}"
            else:
                ok = True
                error = None

        except requests.exceptions.Timeout:
            error = "Превышено время ожидания запроса"
        except requests.exceptions.ConnectionError:
            error = "Ошибка подключения к серверу"
        except requests.exceptions.HTTPError as err:
            error = f"HTTP-ошибка: {err}"
        except requests.exceptions.RequestException as err:
            error = f"Произошла ошибка при выполнении запроса: {err}"
        except requests.exceptions.JSONDecodeError:
            error = "Ошибка при декодировании JSON-ответа"
        finally:
            if ok:
                return RequestResponse(
                    ok=ok,
                    error=error,
                    data=Card(
                        card_id=data.get("cardId"),
                        card_registration_number=data.get("cardRegistrationNumber"),
                        benefit_code=data.get("benefitCode"),
                        benefit_name=data.get("benefitName"),
                        beneficiary_date_from=data.get("beneficiaryDateFrom"),
                        beneficiary_date_to=data.get("beneficiaryDateTo"),
                        card_number=data.get("cardNumber"),
                        balance_amount_cent=data.get("balanceAmountCent"),
                        can_be_refilled=data.get("canBeRefilled"),
                        can_buy_refills_today=data.get("canBuyRefillsToday"),
                        can_balance_be_topped_up=data.get("canBalanceBeToppedUp"),
                        refill_cost_cent=data.get("refillCostCent"),
                        refills=data.get("refills"),
                        periods_available_to_refill=data.get("periodsAvailableToRefill"),
                        order_history=[
                            Order(
                                order_id=order.get("orderId"),
                                amount_cent=order.get("amountCent"),
                                date_purchase=order.get("datePurchase"),
                                order_type_friendly_name=order.get("orderTypeFriendlyName"),
                                fp=order.get("fp")
                            ) for order in data.get("orderHistory", [])
                        ],
                        tripHistory=[
                            Trip(
                                ticket_order_id=trip.get("ticketOrderId"),
                                route_number=trip.get("routeNumber"),
                                route_name=trip.get("routeName"),
                                vehicle_type_name=trip.get("vehicleTypeName"),
                                vehicle_gov_number=trip.get("vehicleGovNumber"),
                                carrier_name=trip.get("carrierName"),
                                total_amount_cent=trip.get("totalAmountCent"),
                                tickets_count=trip.get("ticketsCount"),
                                fp=trip.get("fp"),
                                date_trip=trip.get("dateTrip"),
                                date_trip_string=trip.get("dateTripString"),
                                pos_number=trip.get("posNumber")
                            ) for trip in data.get("tripHistory", [])
                        ],
                        date_expire=data.get("dateExpire"),
                        card_release=data.get("cardRelease")
                    )
                )
            else:
                return RequestResponse(
                    ok=ok,
                    error=error,
                    data=None
                )


if __name__ == "__main__":
    api = API()
    response = api.card_check(card_number=215050004534)
    print(response)

    response = api.get_top_up_link(card_id=response.data.card_id, amount_cent=10000)
    print(response)

    response = api.get_order_status(order_id=response.data.order_id)
    print(response)
