from django.urls import path
from order import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'admin/order', views.OrderAdminView, basename='admin-order')
router.register(r'admin/order-item', views.OrderItemAdminView, basename='admin-order-item')
router.register(r'admin/basket', views.BasketAdminView, basename='admin-basket')
router.register(r'admin/basket-item', views.BasketItemAdminView, basename='admin-basket-item')

urlpatterns = [
    path("order/", views.OrderGetView.as_view(), name="order"),
    path("order/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("basket/", views.BasketGetView.as_view(), name="basket"),
    path('basket/item/create/', views.BasketItemCreateView.as_view(), name='basket-item-create'),
    path('address/', views.AddressListView.as_view(), name='address'),  
]

urlpatterns += router.urls