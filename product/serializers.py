from rest_framework import serializers
from product import models

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = [
            'image'
        ]

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    product_image = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = ['name', 'price', 'description', 'category', 'count', 'product_image']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = models.Category
        fields = ['name', 'products']
    