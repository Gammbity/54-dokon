from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('admin/', admin.site.urls),
   path('ckeditor/', include('ckeditor_uploader.urls')),
   path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
   path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
   #app
   path('api/v1/user/', include('user.urls')),
   path('api/v1/product/', include('product.urls')),
   path('api/v1/order/', include('order.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += debug_toolbar_urls()