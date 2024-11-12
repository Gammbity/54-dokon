from rest_framework import generics
from product import models
from product import serializers

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

#     def create(self, request, *args, **kwargs):
#         comment = models.Comment.objects.