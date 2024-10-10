from user.models import User, UsersPassword
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from user.serializers import UserSerializer, RegistrationSerializer, RegistrationBotSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken

class MeView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer  
    lookup_field = 'pk' 
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class RegistrationView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.save(), status=status.HTTP_201_CREATED)
    
class RegistrationWithBotView(GenericAPIView):
    serializer_class = RegistrationBotSerializer
    
    def post(self, request, *args, **kwargs):
        password = request.data['password']
        generatepasswords = UsersPassword.objects.filter(password=password)
        if password:
            if generatepasswords:
                for generatepassword in generatepasswords:
                    if (now() - generatepassword.time).total_seconds() < 60:
                        refresh_token = RefreshToken.for_user(generatepassword.user)
                        return Response({
                                'refresh': str(refresh_token),
                                'access': str(refresh_token.access_token)
                            })
                    return Response("Parolning faollik muddati 1 daqiqa!")
            return Response("Parol noto'g'ri!", status=status.HTTP_400_BAD_REQUEST) 
        return Response("Parol hali yaratilmagan!", status=status.HTTP_400_BAD_REQUEST)
    
    



