"""lemon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from order.views import OrderCreateAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Order API",
        default_version="v1",
        description=(
            "The Order API allows users to create trading orders programmatically"
        ),
    ),
    public=True,
)

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("schema-redoc"))),
    path("orders/", OrderCreateAPIView.as_view(), name="orders-create"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
