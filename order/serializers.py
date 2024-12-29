from order.models import Order, Basket, OrderItem
from rest_framework import serializers
from product.serializers import ProductSerializer
from django.utils.translation import gettext_lazy as _
from product.models import Product

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
    price = serializers.IntegerField(read_only=True)
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
        products = {}
        try:
            for item_data in items_data:
                product = Product.objects.get(name=item_data['product'])
                products[item_data['product']] = product
                if item_data['quantity'] > product.count:
                    raise serializers.ValidationError(_("Ushbu mahsulotlar soni yetarli emas!"))
            order = Order.objects.create(user=user, **validated_data)
            total_price = 0
            for item_data in items_data:
                product = products[item_data['product']]
                item_data['price'] = product.price * item_data['quantity']
                total_price += item_data['price'] 
                product.count -= item_data['quantity']
                product.save()
                OrderItem.objects.create(order=order, **item_data)
            order.total_price = total_price
            order.save()
            products.clear()
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return order