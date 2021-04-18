from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView

from lemon.order.models import Order
from lemon.order.serializers import OrderSerializer


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema()
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
