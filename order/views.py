from order import models, serializers
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

class AddressListView(generics.ListAPIView):
    serializer_class = serializers.AddressSerializer

    def get_queryset(self):
        return models.Address.objects.filter(user=self.request.user)

class BasketItemCreateView(generics.CreateAPIView):
    serializer_class = serializers.BasketItemCreateSerializer
    queryset = models.BasketItem
    
class OrderGetView(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        basket = models.Basket.objects.get(user=self.request.user)
        basket_items = basket.items.filter(basket=basket)
        return models.Order.objects.filter(user=self.request.user) 
    
class OrderCreateView(generics.CreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.OrderCreateSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        address = serializer.validated_data["address"]

        basket = models.Basket.objects.filter(user=user).first()
        basket_items = basket.items.all()

        order = models.Order.objects.create(user=user, address=address)
        total_price = 0

        for item in basket_items:
            product = item.product
            item_price = product.price * item.quantity
            total_price += item_price
            product.count -= item.quantity
            product.save()
            models.OrderItem.objects.create(order=order, product=product, price=item_price, quantity=item.quantity)

        order.total_price = total_price
        order.save()

        basket.clean()

        return Response({"message": _("Buyurtma yaratildi!"), "order_id": order.id}, status=status.HTTP_201_CREATED)
        
    
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


    