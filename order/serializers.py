from order.models import Order, Basket, OrderItem, BasketItem, Address, Status
from rest_framework import serializers
from product.serializers import ProductSerializer
from django.utils.translation import gettext_lazy as _
from product.models import Product
from user.models import User


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
        basket = Basket.objects.get(user=user)
        try:
            product = Product.objects.get(id=validated_data['product'])
            if product.count < validated_data['quantity']:
                raise serializers.ValidationError(_("Ushbu mahsulotlar soni yetarlicha emas!"))
            basket_item = BasketItem.objects.create(
                basket=basket,
                product=product,
                quantity=validated_data['quantity']
            )
            basket.total_price += product.price * int(validated_data['quantity'])
            basket.save()
            return basket_item
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
    longitude = serializers.FloatField(required=False, allow_null=True)
    latitude = serializers.FloatField(required=False, allow_null=True)
    location = serializers.CharField(required=False, allow_null=True)
    class Meta:
        model = Address
        fields = ['longitude', 'latitude', 'location']

class OrderSerializer(serializers.ModelSerializer):
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
    existing_addresses = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.none(), required=False, allow_null=True
    )
    address = AddressSerializer(required=False, allow_null=True)
    class Meta:
        model = Order
        fields = [
            'existing_addresses',
            'address'
        ]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)

        if request and hasattr(request, 'user'):
            fields['existing_addresses'].queryset = Address.objects.filter(user=request.user)
        return fields

    def validate(self, data):
        existing_addresses = data.pop('existing_addresses')
        address = data.pop('address')
        if not existing_addresses and not address:
            raise serializers.ValidationError({"address": _("Joylashuv kiritilishi kerak!")})
        elif address and address['location']:
            new_address = Address.objects.create(
                user=self.context['request'].user, **address 
            ) 
            data['id'] = new_address.id
        else:
            existing_addresse = Address.objects.filter(location=existing_addresses).first()
            data['id'] = existing_addresse.id
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        products = {}
        basket = Basket.objects.filter(user=user).first()
        if not basket:
            raise serializers.ValidationError({"basket":_("Savatcha hali mavjud emas!")})
        basket_items = basket.items.filter(basket=basket).all()     
        if not basket_items:
            raise serializers.ValidationError({"basket_items":_("Savatcha elementlari hali mavjud emas!")})
        try:
            for item_data in basket_items:
                product = Product.objects.get(name=item_data.product)
                products[item_data.product] = product
                if item_data.quantity > product.count:
                    raise serializers.ValidationError(_("Ushbu mahsulotlar soni yetarli emas!"))
            address = Address.objects.get(id=validated_data['id'])
            user = User.objects.get(username=user)
            order = Order.objects.create(user=user, address=address)
            total_price = 0
            for item_data in basket_items:
                product = products[item_data.product]
                item_data.price = product.price * item_data.quantity
                total_price += item_data.price 
                product.count -= item_data.quantity
                product.save()
                OrderItem.objects.create(order=order, product=product, price=item_data.price, quantity=item_data.quantity)
            order.total_price = total_price
            order.save()
            products.clear()
            basket.clean()
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return order