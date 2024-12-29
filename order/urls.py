from django.urls import path
from order import views

urlpatterns = [
    path("orders/", views.OrderListView.as_view(), name="orders"),
    path("order/<int:pk>/", views.OrderGetView.as_view(), name="order"),
    path("order/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("basket/", views.BasketListView.as_view(), name="basket"),
    path("basket/create/", views.BasketCreateView.as_view(), name="basket-create"),
]
