from datetime import datetime

from drf_yasg import openapi


class OrderAPICustomSchmema:
    description = (
        "Create an order to buy or sell a positive, non-zero quantity of any valid "
        "instrument that can be uniquely identified via ISIN."
    )

    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "isin": openapi.Schema(
                type=openapi.TYPE_STRING,
                title="isin",
                pattern=r"^[a-zA-Z]{2}[a-zA-Z0-9]{9}\d{1}$",
                description="ISIN of a valid instrument",
                minLength=12,
                maxLength=12,
            ),
            "limit_price": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                title="limit_price",
                format="decimal",
                description="Order will be executed when the limit price is reached",
                minimum=-0.01,
            ),
            "quantity": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                title="quantity",
                description="Quantity of shares to buy or sell",
                minimum=1,
            ),
            "side": openapi.Schema(
                type=openapi.TYPE_STRING,
                title="side",
                enum=["buy", "sell"],
                description="Buy or sell shares",
            ),
            "valid_until": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                title="valid_until",
                description="UTC Unix Timestamp. Must be in the future",
                minimum=int(datetime.utcnow().timestamp()),
            ),
        },
        required=["isin", "quantity", "side", "valid_until"],
    )

    responses = {
        201: openapi.Response(
            "Order created",
            request_body,
            examples={
                "application/json": {
                    "isin": "US88160R1014",
                    "limit_price": 100.99,
                    "quantity": 10,
                    "side": "buy",
                    "valid_until": 2147483647,
                }
            },
        ),
        400: openapi.Response(
            "Bad Request",
            examples={
                "application/json": {
                    "isin": [
                        "Ensure this field has at least 12 characters.",
                        "This value does not match the required pattern.",
                    ]
                }
            },
        ),
    }
