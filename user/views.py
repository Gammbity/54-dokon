from user.models import User, UsersPassword
from user import serializers

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password, make_password

from datetime import datetime
from config.settings import SECRET_KEY
from datetime import timedelta
import jwt

def response_token_cookie(user, message):
    refresh_token = RefreshToken.for_user(user)
    access = {str(refresh_token.access_token)}
    response = Response({'access_token': access}, message)
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
        except User.DoesNotExist:
            return Response({"message": _(f"{username} ushbu username mavjud emas")}, status=status.HTTP_400_BAD_REQUEST)
        if check_password(password, user.password):
            login(request, user)
            response = response_token_cookie(user, 200)
            return response
        else: return Response({"message": _("Parol noto'g'ri")}, status=status.HTTP_400_BAD_REQUEST)
         
class LogOutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        response = Response({'message':_("Tizimdan chiqish muvaffaqiyatli amalga oshirildi")})
        response.delete_cookie('refresh_token')
        request.session.flush()
        return response

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class =serializers.RegistrationSerializer

    def post(self, request, *args, **kwargs):

        """
        Ro'yxatdan o'tish va tizimga kirish
        ---
        # Parameters
        None
        
        # Example
        {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone": "+998901234567",
            "password": "12345678"
        }
        # Response
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3MjM2NjQ3LCJpYXQiOjE2MjcxNTA2NDcsImp0aSI6IjIwZjg2ZjRhMTQ3YjRmMjk2ZmM2NmU2YjY4NWVlODk5IiwidXNlcl9pZCI6MX0._V3f4gZ7JtQXb2hT9hVTLv4vUO9yUk6XN2XfJjZl3Qs"
        }
        # Status
        201 Created
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        if user.is_authenticated:
            response = response_token_cookie(user, 201)   
            return response
        else: raise AuthenticationFailed(status.HTTP_400_BAD_REQUEST)  
        
class LoginWithBotView(generics.GenericAPIView):
    serializer_class = serializers.RegistrationBotSerializer
    
    def post(self, request, *args, **kwargs):
        if request.data['password']:
            password = int(request.data['password'])
            generatepassword = UsersPassword.objects.filter(password=password).first()
            if generatepassword:
                time_diff = int((now() - generatepassword.time).total_seconds())
                if time_diff <= 10000:
                    user = generatepassword.user
                    response = response_token_cookie(user, 201)
                    return response
                else:return Response(_("Parolning faollik muddati 1 daqiqa!"), status=status.HTTP_400_BAD_REQUEST)
            else:return Response(_("Parol noto'g'ri!"), status=status.HTTP_400_BAD_REQUEST) 
        else:return Response(_("Parol hali yaratilmagan!"), status=status.HTTP_400_BAD_REQUEST)

class MeView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer  
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user    
        
class UsernamePasswordEditView(generics.GenericAPIView):
    serializer_class = serializers.UsernamePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        username = user.username
        if username:
            return Response({"username": username})
        else:
            return Response({"username": ""})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        password = request.data.get('password')
        username = request.data.get('username')
        new_password = request.data.get('new_password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(_("Username yoki Parol xato!"))
        if username and new_password:
            user.username = username
            user.password = make_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        user.password = request['new_password']
        user.save()
        return Response(status.HTTP_200_OK)
    