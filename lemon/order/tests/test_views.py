from decimal import Decimal

import pytest
from django.urls import reverse_lazy
from order.models import Order
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def url_orders_create() -> str:
    return reverse_lazy("orders-create")


@pytest.fixture
def valid_order() -> dict:
    return {
        "isin": "US88160R1014",
        "limit_price": 100.99,
        "quantity": 1,
        "side": "buy",
        "valid_until": 2147483647,
    }


@pytest.mark.django_db
def test_can_post_valid_order(
    api_client: APIClient, url_orders_create: str, valid_order: dict
):
    response = api_client.post(path=url_orders_create, data=valid_order, format="json")

    assert response.status_code == 201
    assert response.json() == {"id": 1, **valid_order}


@pytest.mark.django_db
def test_can_post_valid_order_creates_db_model(
    api_client: APIClient, url_orders_create: str, valid_order: dict
):
    response = api_client.post(path=url_orders_create, data=valid_order, format="json")

    assert response.status_code == 201
    assert Order.objects.count() == 1

    order = Order.objects.first()

    assert order.isin == valid_order["isin"]
    assert order.limit_price == round(Decimal(valid_order["limit_price"]), 2)
    assert order.quantity == valid_order["quantity"]
    assert order.side == valid_order["side"]
    assert order.valid_until == valid_order["valid_until"]


@pytest.mark.django_db
def test_validation_error_returns_405(
    api_client: APIClient, url_orders_create: str, valid_order: dict
):
    valid_order.update({"isin": "invalid"})
    response = api_client.post(path=url_orders_create, data=valid_order, format="json")

    assert response.status_code == 400
    assert Order.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "side", [{"side": "BUY"}, {"side": "buY"}, {"side": "SELL"}, {"side": "sElL"}]
)
def test_param_side_is_case_insensitive(
    api_client: APIClient, url_orders_create: str, valid_order: dict, side: dict
):
    valid_order.update(side)
    response = api_client.post(path=url_orders_create, data=valid_order, format="json")

    assert response.status_code == 201
    assert response.json()["side"] == side["side"].lower()


@pytest.mark.django_db
def test_param_limit_price_can_be_number_or_string(
    api_client: APIClient, url_orders_create: str, valid_order: dict
):
    # Since we're storing "limit_price" as Decimal, we should be able to use both
    # floats and strings in the POST payload

    valid_order.update({"limit_price": str(valid_order["limit_price"])})
    response = api_client.post(path=url_orders_create, data=valid_order, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_other_http_methods_are_not_allowed(
    api_client: APIClient, url_orders_create: str
):

    assert api_client.get(path=url_orders_create).status_code == 405
    assert api_client.get(path=url_orders_create).json() == {
        "detail": 'Method "GET" not allowed.'
    }

    assert api_client.put(path=url_orders_create).status_code == 405
    assert api_client.put(path=url_orders_create).json() == {
        "detail": 'Method "PUT" not allowed.'
    }

    assert api_client.patch(path=url_orders_create).status_code == 405
    assert api_client.patch(path=url_orders_create).json() == {
        "detail": 'Method "PATCH" not allowed.'
    }
