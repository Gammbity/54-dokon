from order.models import Order
from rest_framework import serializers

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
            'user',
            'product',
            'quantity',
            'longitude',
            'latitude',
            'location',
        ]
        read_only_fields = ['user']