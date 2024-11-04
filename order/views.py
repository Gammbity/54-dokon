from django.shortcuts import render
from order import models, serializers
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class OrderListView(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user) 
    
class OrderGetView(generics.RetrieveAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user) 
    
class OrderCreateView(generics.CreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderCreateSerializer
    permission_classes = [IsAuthenticated]
        
    
class BasketListView(generics.ListAPIView):
    serializer_class = serializers.BasketSerializer

    def get_queryset(self):
        return models.Basket.objects.filter(user=self.request.user)

class BasketCreateView(generics.CreateAPIView):
    queryset = models.Basket.objects.all()
    serializer_class = serializers.BasketCreateSerializer

    