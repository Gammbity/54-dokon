from rest_framework import serializers
from product import models

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['user', 'text', 'degree', 'created_at']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['text', 'product', 'degree']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image']

class ProductSerializer(serializers.ModelSerializer):
    comment = CommentSerializer
    category = serializers.CharField()
    product_image = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = models.Product
        fields = ['name', 'with_rebate', 'description', 'category', 'count', 'views', 'likes', 'product_image', 'comment', 'created_at']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = models.Category
        fields = ['name', 'products']
