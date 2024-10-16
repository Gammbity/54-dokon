from order.models import Order, Basket
from rest_framework import serializers
from product.serializers import ProductSerializer

class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Basket
        fields = ['product']

class BasketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ['product']

    def create(self, validated_data):
        user = self.context['request'].user
        basket = Basket.objects.create(user=user, **validated_data)
        return basket

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'quantity',
            'longitude',
            'latitude',
            'location',
            'status',
            'total_price',
            'created_at',
            'updated_at',
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'product',
            'quantity',
            'longitude',
            'latitude',
            'location',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        return order