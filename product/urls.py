from django.urls import path

from rest_framework.routers import DefaultRouter

from product import views

router = DefaultRouter()
router.register(r'admin/products', views.AdminProductView, basename='admin-product'),
router.register(r'admin/category', views.AdminCategoryView, basename='admin-category'),

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="products"),
    path("product/<str:slug>/", views.ProductView.as_view(), name="product"),
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("category/<str:slug>/", views.CategoryView.as_view(), name="category"),

    # path('comment/delete/', views.CommentDelView.as_view(), name='comment-delete'),
    # path('comment/create/', views.CommentCreateView.as_view(), name='comment-create'),    
]

urlpatterns += router.urls