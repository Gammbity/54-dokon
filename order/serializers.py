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
    order_item = OrderItemCreateSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'longitude',
            'latitude',
            'location',
            'order_item'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('order_item')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        total_price = 0
        for item_data in items_data:
            total_price += item_data['price'] * item_data['quantity']
            OrderItem.objects.create(order=order, **item_data)
        order.total_price = total_price
        order.save()
        return order
    
    
    """
    
    {
        "longitude": "12.340000",
        "latitude": "34.210000",
        "location": "Uzbekistan/Tashkent/Gisht ko'prik 113-uy",
        "order_item": [
            {
                "product": 7,
                "price": 12000,
                "quantity": 1
            },
            {
                "product": 7,
                "price": 2000,
                "quantity": 3
            },
            {
                "product": 7,
                "price": 1000,
                "quantity": 3
            }
        ]
    }   
    
    """
