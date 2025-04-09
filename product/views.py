from product import serializers
from product import models

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404


class ProductListView(generics.ListAPIView):
    queryset = models.Product.objects.order_by('?')
    serializer_class = serializers.ProductSerializer

class ProductView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'

class CategoryListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoriesSerializer

class CategoryView(generics.RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'

# class CommentCreateView(generics.CreateAPIView):
#     serializer_class = serializers.CommentCreateSerializer
#     queryset = models.Comment.objects.all()
#     permission_classes = [IsAuthenticated]

# class CommentDelView(generics.DestroyAPIView):
#     serializer_class = serializers.CommentDelSerializer
    
#     def delete(self, request, *args, **kwargs):
#         comment = get_object_or_404(models.Comment, pk=kwargs['pk'], user=request.user)
#         comment.delete()
#         return Response({"message", "Izoh muvaffaqiyatli o'chirildi"}, status.HTTP_204_NO_CONTENT)

# class CommentListView(generics.ListAPIView):
#     queryset = models.Comment.objects.all()
#     serializer_class = serializers.CommentSerializer

# class CommentGetView(generics.RetrieveAPIView):
#     queryset = models.Comment.objects.all()
#     serializer_class = serializers.CommentSerializer
#     lookup_field = ['slug']



# ADMIN ----------------------------------------------------------------


class AdminProductView(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.AdminProductSerializer
    lookup_field = 'name'

class AdminCategoryView(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.AdminCategorySerializer
    lookup_field = 'name'