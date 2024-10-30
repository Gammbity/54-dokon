from order.models import Order, Basket, OrderItem
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

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'order',
            'price',
            'quantity'
        ]

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'order',
            'price',
            'quantity'
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'longitude',
            'latitude',
            'location',
            'status',
            'total_price',
            'created_at',
            'updated_at',
            'order_item',
        ]
    

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'longitude',
            'latitude',
            'location',
            'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order