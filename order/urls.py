from django.urls import path
from order import views

urlpatterns = [
    path("order/", views.OrderGetView.as_view(), name="order"),
    path("order/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("basket/", views.BasketGetView.as_view(), name="basket"),
    path('basket/item/create/', views.BasketItemCreateView.as_view(), name='basket-item-create'),
]
