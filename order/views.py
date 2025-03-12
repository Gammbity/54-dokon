from order import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# class OrderItemSerializer()

    
class OrderGetView(generics.GenericAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user) 
    
class OrderCreateView(generics.CreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderCreateSerializer
    permission_classes = [IsAuthenticated]
        
    
class BasketGetView(generics.GenericAPIView):
    serializer_class = serializers.BasketSerializer

    def get_queryset(self):
        return models.Basket.objects.filter(user=self.request.user)


    