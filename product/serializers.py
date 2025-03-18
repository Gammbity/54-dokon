from rest_framework import serializers
from product import models
from django.utils.translation import gettext_lazy as _
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            'name',
            'real_price',
            'price',
            'description',
            'count',
            'category',
            'rebate',
            'is_new',
        ]

        def validate(self, data):
            product = models.Product.objects.filter(name=data.name).exists()
            if product:
                raise serializers.ValidationError(_("Ushbu mahsolat allaqachon yaratib bo'lingan"))
            return data

        def create(self, validated_data):
            pass

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = [
            'image',
            'name',
            'subcategory',
        ]

class CommentDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['id']

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
