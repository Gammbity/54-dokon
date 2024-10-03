from user.models import User
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from user.serializers import UserSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class MeView(RetrieveAPIView):
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]  
    lookup_field = 'pk' 

    def get_object(self):
        return self.request.user
    
class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.save(), status=status.HTTP_201_CREATED)
    
    



