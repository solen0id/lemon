from drf_yasg.utils import swagger_auto_schema
from order.models import Order
from order.openapi import OrderAPICustomSchmema
from order.serializers import OrderSerializer
from rest_framework.generics import CreateAPIView


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description=OrderAPICustomSchmema.description,
        responses=OrderAPICustomSchmema.responses,
        request_body=OrderAPICustomSchmema.request_body,
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
