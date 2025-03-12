from order import models, serializers
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

class BasketItemCreateView(generics.CreateAPIView):
    serializer_class = serializers.BasketItemCreateSerializer
    queryset = models.BasketItem
    
class OrderGetView(generics.ListAPIView):
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            basket = models.Basket.objects.get(user=user)
        except models.Basket.DoesNotExist:
            return Response({"error": _("Savatcha toplimadi!")}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(basket) 
        return Response(serializer.data, status=200)


    