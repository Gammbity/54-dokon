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
    
class OrderCreateView(generics.CreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = serializers.OrderCreateSerializer(data=request.data)
        if order.is_valid():
            order.save(user=request.user)
            return Response(order.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)