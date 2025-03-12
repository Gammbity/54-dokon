from django.urls import path
from order import views

urlpatterns = [
    path("order/", views.OrderGetView.as_view(), name="orders"),
    path("order/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("basket/", views.BasketGetView.as_view(), name="basket"),
]
