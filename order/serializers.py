from order.models import Order, Basket, OrderItem, BasketItem, Address, Status
from rest_framework import serializers
from product.serializers import ProductSerializer
from django.utils.translation import gettext_lazy as _
from product.models import Product


class BasketItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    class Meta:
        model = BasketItem
        fields = ['basket_id', "product", "quantity", "price", "created_at", "updated_at"]

class BasketItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    price = serializers.IntegerField(read_only=True)
    class Meta:
        model = BasketItem
        fields = ['product', "quantity", "price"]

    def create(self, validated_data):
        user = self.context['request'].user
        basket = Basket.objects.get(user_id=user)
        try:
            product = Product.objects.get(name=validated_data['product'])
            if product.count < validated_data['quantity']:
                raise serializers.ValidationError(_("Ushbu mahsulotlar soni yetarlicha emas!"))
            basket_item = BasketItem.objects.create(
                basket_id=basket,
                product_id=product,
                quantity=validated_data['quantity'],
                price=validated_data["price"]
            )
            basket_item.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))
        

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ["id", "user_id", "total_price"]


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['product', 'quantity', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'order_id',
            'price',
            'quantity'
        ]
        
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['status']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['longitude', 'latitude', 'location']

class OrderSerializer(serializers.ModelSerializer):
    # order_item = OrderItemSerializer(many=True)
    status = StatusSerializer()
    address = AddressSerializer()
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'address',
            'total_price',
            'created_at',
            'updated_at',
        ]
    

class OrderCreateSerializer(serializers.ModelSerializer):
    order_item = OrderItemCreateSerializer(many=True)
    address = AddressSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'order_item',
            'address'
        ]


    def create(self, validated_data):
        items_data = validated_data.pop('order_item')
        user = self.context['request'].user
        products = {}
        basket = Basket.objects.get(user=user)
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