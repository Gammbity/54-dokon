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
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
import jwt
from datetime import datetime
from config.settings import SECRET_KEY
from datetime import timedelta
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

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
        try:
            auth_header = request.headers.get('X-Refresh-Token')
            print(auth_header)
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({'error': _("Noto'g'ri token1")}, status=status.HTTP_401_UNAUTHORIZED)
            refresh_token = auth_header.split(' ')[1]
            print()
            print(refresh_token)
            token = RefreshToken(refresh_token)
            print(token)
            token.verify()
            token.blacklist()
            response = Response({'message':_("Tizimdan chiqish muvaffaqiyatli amalga oshirildi")})
            response.delete_cookie('refresh_token', samesite='Strict', secure=True)
            request.session.flush()
            return response
        except (InvalidToken, TokenError):
            return Response({"error": "Noto'g'ri token"}, status=status.HTTP_401_UNAUTHORIZED)

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class =serializers.RegistrationSerializer

    def post(self, request):
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
            generatepassword = UsersPassword.objects.get(password=password)
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

class RefreshTokenView(generics.CreateAPIView):
    serializer_class = serializers.RefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        token = request.data.get('refresh_token')
        if token:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            exp_time = datetime.fromtimestamp(payload['exp']) # 'exp': 1732280262, 1970-yil 1-yanvar 00:00:00 UTC dan boshlab soniyalarda hisoblangan vaqtni ko'rsatadi.
            if exp_time > datetime.now() - timedelta(days=10):
                token = RefreshToken(token)
                token.blacklist()
                new_token = RefreshToken.for_user(request.user)
                return Response({'access_token': str(new_token.access_token)}, status.HTTP_200_OK)
            else: 
                return Response({"message": _("Token muddati o'tib ketgan")})
        else:
            return Response({"message": _("refresh_token mavjud emas")}) 
        
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
        username = request['username']
        password = request['password']
        if username and password:
            user.username = username
            user.password = password
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
    