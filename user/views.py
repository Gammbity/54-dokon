from user.models import User, UsersPassword
from rest_framework import generics
from user import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
import jwt
from datetime import datetime
from config.settings import SECRET_KEY
from datetime import timedelta

def response_token_cookie(request):
    refresh_token = RefreshToken.for_user(request.user)
    response = Response({"access_token": str(refresh_token.access_token), "message": _("Muvaffaqiyatli amalga oshirildi")})
    response.set_cookie(
        key="refresh_token",
        value=str(refresh_token),
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=3600
    )
    return response

class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"message": _("username va parolni kiritish majburiy")}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                return response_token_cookie(request)
            else: return Response({"message": "Parol noto'g'ri"}, status=status.HTTP_400_BAD_REQUEST)
        except:  
            return Response({"message": _(f"{username} ushbu username mavjud emas")}, status=status.HTTP_400_BAD_REQUEST)

class LogOutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        response = Response({"message": _("Tizimdan chiqish muvaffaqiyatli amalga oshirildi")})
        response.delete_cookie('refresh_token')
        return response

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class =serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.user:
            return response_token_cookie(request)
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
    
class RegistrationWithBotView(generics.GenericAPIView):
    serializer_class = serializers.RegistrationBotSerializer
    
    def post(self, request, *args, **kwargs):
        password = request.data['password']
        generatepasswords = UsersPassword.objects.filter(password=password)
        if password:
            if generatepasswords:
                for generatepassword in generatepasswords:
                    if (now() - generatepassword.time).total_seconds() < 60:
                        return response_token_cookie(generatepassword)
                    return Response(_("Parolning faollik muddati 1 daqiqa!"))
            return Response(_("Parol noto'g'ri!"), status=status.HTTP_400_BAD_REQUEST) 
        return Response(_("Parol hali yaratilmagan!"), status=status.HTTP_400_BAD_REQUEST)

class MeView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer  
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user    

class RefreshTokenView(generics.CreateAPIView):
    serializer_class = serializers.RefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        token = request.data['refresh_token']
        if token:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            exp_time = datetime.fromtimestamp(payload['exp']) # 'exp': 1732280262, 1970-yil 1-yanvar 00:00:00 UTC dan boshlab soniyalarda hisoblangan vaqtni ko'rsatadi.
            if exp_time > datetime.now() - timedelta(days=10):
                token = RefreshToken.for_user(request.user)
                return Response({'refresh_token': str(token.access_token)}, status.HTTP_200_OK)
            else: 
                return Response({"message": _("Token muddati o'tib ketgan")})
        else:
            return Response({"message": _("refresh_token mavjud emas")}) 
        
