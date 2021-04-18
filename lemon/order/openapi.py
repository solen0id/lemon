from drf_yasg import openapi

from lemon.order.serializers import OrderSerializer


class OrderAPICustomSchmema:
    description = (
        "Create an order to buy or sell a positive, non-zero quantity of any valid "
        "instrument that can be uniquely identified via ISIN."
    )

    responses = {
        201: openapi.Response("Order created", OrderSerializer),
        405: openapi.Response("Validation Error"),
    }
