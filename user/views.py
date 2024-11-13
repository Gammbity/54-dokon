from user.models import User, UsersPassword
from rest_framework.generics import RetrieveAPIView, CreateAPIView, GenericAPIView
from user.serializers import UserSerializer, RegistrationSerializer, RegistrationBotSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.http import JsonResponse
        
class LogOutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"message": "Logout seccessfully"})


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.user:
            token = RefreshToken.for_user(request.user)
            response = Response({"token" :str(token.access_token)}, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='refresh_token',
                value=str(token),
                httponly=True,
                secure=True, 
                samesite='Strict',
                max_age=3600
            )
            return response
        else: raise AuthenticationFailed(status.HTTP_400_BAD_REQUEST)  
        

        """{
            "first_name": "Abduboriy",
            "last_name": "Abdusamatov",
            "username": "admin1",
            "email": "a1@g.com",
            "phone": "+998880334626",
            "password": "Qwerty123$",
            "telegram_id": null
            }
    """
    
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
                    return Response(_("Parolning faollik muddati 1 daqiqa!"))
            return Response(_("Parol noto'g'ri!"), status=status.HTTP_400_BAD_REQUEST) 
        return Response(_("Parol hali yaratilmagan!"), status=status.HTTP_400_BAD_REQUEST)

class MeView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer  
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user    
    
