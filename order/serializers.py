from order.models import Order, Basket, OrderItem, BasketItem, Address, Status
from rest_framework import serializers
from product.serializers import ProductSerializer
from django.utils.translation import gettext_lazy as _
from product.models import Product
from user.models import User
from user.serializers import UserSerializer


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
        fields = ['existing_addresses', 'address']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)

        if request and hasattr(request, 'user'):
            fields['existing_addresses'].queryset = Address.objects.filter(user=request.user)
        return fields
    
    def validate(self, data):
        user = self.context["request"].user

        existing_addresses = data.get("existing_addresses")
        address = data.get("address")

        if not existing_addresses and not address:
            raise serializers.ValidationError({"address": _("Joylashuv kiritilishi kerak!")})

        if address:
            if not isinstance(address, dict) or "location" not in address:
                raise serializers.ValidationError({"address": _("Manzil noto‘g‘ri formatda!")})

        data["address"] = existing_addresses or Address.objects.create(user=user, **address)

        basket = Basket.objects.filter(user=user).prefetch_related("items__product").first()
        if not basket:
            raise serializers.ValidationError({"basket": _("Savatcha hali mavjud emas!")})

        basket_items = basket.items.all()
        if not basket_items:
            raise serializers.ValidationError({"basket_items": _("Savatcha elementlari hali mavjud emas!")})

        for item in basket_items:
            if item.quantity > item.product.count:
                raise serializers.ValidationError({f"product_{item.product.id}": _("Ushbu mahsulotlar soni yetarli emas!")})

        return data
    
# ADMIN ---------------------------------------------------------

class OrderAdminSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    status = StatusSerializer
    address = AddressSerializer(read_only=True)
    total_price = serializers.IntegerField(read_only=True)
    class Meta:
        model = Order
        fields = ['user', 'status', 'address', 'total_price', 'created_at', 'updated_at']

class OrderItemAdminSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    order = serializers.CharField(read_only=True)
    class Meta:
        model = OrderItem
        fields = ["product", "order", "price", "quantity", "created_at", "updated_at"]

class BasketAdminSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    total_price = serializers.IntegerField(read_only=True)
    class Meta:
        model = Basket
        fields = ['user', 'total_price', 'created_at', 'updated_at']

class BasketItemAdminSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    basket = serializers.CharField(read_only=True)
    class Meta:
        model = BasketItem
        fields = ["product", "basket", "price", "quantity", "created_at", "updated_at"]