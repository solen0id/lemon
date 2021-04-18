import re

import pytest
from rest_framework.serializers import ValidationError as DRFValidationError

from lemon.order.serializers import OrderSerializer


@pytest.fixture
def valid_order():
    return {
        "isin": "DE1234ABCDE0",
        "limit_price": 100.99,
        "quantity": 1,
        "side": "buy",
        "valid_until": 2147483647,
    }


@pytest.mark.parametrize(
    "order, expected_error",
    [
        (
            {
                "isin": "",
                "limit_price": "",
                "quantity": "",
                "side": "",
                "valid_until": "",
            },
            re.escape(
                "{'isin': [ErrorDetail(string='This field may not be blank.', code='blank')], 'quantity': [ErrorDetail(string='A valid integer is required.', code='invalid')], 'side': [ErrorDetail(string='This field may not be blank.', code='blank')], 'valid_until': [ErrorDetail(string='A valid integer is required.', code='invalid')]}"
            ),
        ),
        (
            {
                "isin": None,
                "limit_price": None,
                "quantity": None,
                "side": None,
                "valid_until": None,
            },
            re.escape(
                "{'isin': [ErrorDetail(string='This field may not be null.', code='null')], 'quantity': [ErrorDetail(string='This field may not be null.', code='null')], 'side': [ErrorDetail(string='This field may not be null.', code='null')], 'valid_until': [ErrorDetail(string='This field may not be null.', code='null')]}"
            ),
        ),
        (
            {"isin": "AB12345678910"},
            re.escape(
                "{'isin': [ErrorDetail(string='Ensure this field has no more than 12 characters.', code='max_length'), ErrorDetail(string='This value does not match the required pattern.', code='invalid')]}"
            ),
        ),
        (
            {"isin": "AB123456789"},
            re.escape(
                "{'isin': [ErrorDetail(string='Ensure this field has at least 12 characters.', code='min_length'), ErrorDetail(string='This value does not match the required pattern.', code='invalid')]}"
            ),
        ),
        (
            {"limit_price": -1},
            re.escape('The value of "limit_price" must be greater than 0'),
        ),
        (
            {"limit_price": 0},
            re.escape('The value of "limit_price" must be greater than 0'),
        ),
        ({"quantity": -1}, re.escape('The value of "quantity" must be greater than 0')),
        ({"quantity": 0}, re.escape('The value of "quantity" must be greater than 0')),
        ({"quantity": 1.5}, re.escape("A valid integer is required.")),
        (
            {"side": "loan"},
            re.escape('The value of "side" must be either "buy" or "sell"'),
        ),
        (
            {"valid_until": 1609455600},  # Fri Jan 01 2021 00:00:00 GMT+0100 (
            re.escape(
                'The value of "valid_until" must be a UNIX timestamp in the future'
            ),
        ),
        ({"valid_until": 1618755523.555555}, re.escape("A valid integer is required.")),
    ],
)
def test_order_serializer(order: dict, expected_error: str, valid_order: dict):
    valid_order.update(order)
    with pytest.raises(DRFValidationError, match=expected_error):
        OrderSerializer(data=valid_order).is_valid(raise_exception=True)
