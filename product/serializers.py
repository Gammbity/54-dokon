from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from product import models

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['user', 'text', 'degree', 'created_at']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image']
    
class CommentDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['id']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['text', 'product', 'degree']

class ProductSerializer(serializers.ModelSerializer):
    comment = CommentSerializer
    category = serializers.CharField()
    product_image = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = models.Product
        fields = ['name', 'with_rebate', 'description', 'category', 'count', 'views', 'likes', 'product_image', 'comment', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = models.Category
        fields = ['name', 'products', 'subcategory']


# ADMIN -------------------------------------------------------------------------------

class AdminProductSerializer(serializers.ModelSerializer):
    comment = CommentSerializer
    category = CategoriesSerializer
    product_image = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = models.Product
        fields = ['name', "real_price", "price", 'with_rebate', 'description', 'category', 'count', 'views', 'likes', "rebate", 'product_image', "is_new", 'comment', 'created_at']


    def validate_name(self, value):
        product = models.Product.objects.filter(name=value).exists()
        if product:
            raise serializers.ValidationError(_("Ushbu mahsolat allaqachon yaratib bo'lingan"))
        return value
    
    def validate_category(self, value):
        if not models.Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(_("Berilgan kategoriya mavjud emas."))

class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = [
            'image',
            'name',
            'subcategory',
            'created_at',
        ]

    def validate_name(self, value):
        category = models.Category.objects.filter(name=value).exists()
        if category:
            raise serializers.ValidationError(_("Ushbu kategoriya allaqachon yaratib bo'lingan"))
        return value