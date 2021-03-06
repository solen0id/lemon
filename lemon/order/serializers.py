from datetime import datetime
from decimal import Decimal
from typing import Optional, Union

from order.models import SIDES, Order
from rest_framework import serializers
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        swagger_schema_fields = {"isin": "ISIN12345"}

    isin = serializers.RegexField(
        regex=r"^[a-zA-Z]{2}[a-zA-Z0-9]{9}\d{1}$",
        required=True,
        min_length=12,
        max_length=12,
    )
    limit_price = serializers.DecimalField(
        required=False,
        allow_null=True,
        coerce_to_string=False,
        max_digits=19,
        decimal_places=2,
    )
    quantity = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={"min_value": 'The value of "quantity" must be greater than 0.'},
    )
    side = serializers.CharField(required=True)
    valid_until = serializers.IntegerField(required=True)

    def validate_limit_price(self, value: Optional[Union[str, float]]):
        if value is not None and Decimal(value) <= Decimal("0.00"):
            raise serializers.ValidationError(
                'The value of "limit_price" must be greater than 0.'
            )
        return value

    def validate_side(self, value: str):
        if value.lower() not in SIDES.values:
            raise serializers.ValidationError(
                'The value of "side" must be either "buy" or "sell".'
            )
        return value.lower()

    def validate_valid_until(self, value: int):
        if value <= datetime.utcnow().timestamp():
            raise serializers.ValidationError(
                'The value of "valid_until" must be a UNIX timestamp in the future.'
            )
        return value
