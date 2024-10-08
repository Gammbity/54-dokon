from rest_framework import serializers
from product import models

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    class Meta:
        model = models.Product
        fields = [
            'name',
            'price',
            'description',
            'category',
        ]

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = models.Category
        fields = ['name', 'products']
    