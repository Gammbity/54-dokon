from django.urls import path
from product import views

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="products"),
    path("product/<int:pk>/", views.ProductView.as_view(), name="product"),
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("category/<int:pk>/", views.CategoryView.as_view(), name="category"),    
]
