from django.urls import path
from order import views

urlpatterns = [
    path("orders/", views.OrderListView.as_view(), name="orders"),
    path("order/create/", views.OrderCreateView.as_view(), name="order-create"),
]
