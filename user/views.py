from config.settings import SECRET_KEY

from user.models import User, UsersPassword
from user import serializers

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password, make_password


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
			refresh_token = request.COOKIES.get('refresh_token')
			if refresh_token:
				token = RefreshToken(refresh_token)
				token.blacklist() 

			response = Response({'message': _("Tizimdan chiqish muvaffaqiyatli amalga oshirildi")})
			response.delete_cookie('refresh_token')
			request.session.flush()
			return response
		except Exception as e:
			return Response({"error": str(e)}, status=400)

class RegistrationView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class =serializers.RegistrationSerializer

	def post(self, request, *args, **kwargs):
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
	queryset = User.objects.all()
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
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		password = request.data.get('password')
		username = request.data.get('username')
		new_password = serializer.validated_data.get('password1')
		is_same = check_password(password, user.password)
		if not is_same:
			raise serializers.ValidationError(_("Parol xato!"))
		user.username = username if username else user.username
		user.password = make_password(new_password) if make_password(new_password) else password
		user.save()
		return Response(status=status.HTTP_200_OK)

class UserAdminView(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = serializers.UserAdminSerializer
	http_method_names = ['get', 'delete']
	permission_classes = [IsAdminUser]

class ChangeUserPermissionView(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = serializers.ChangeUserPermissionSerializer
	permission_classes = [IsAdminUser]

	def post(self, request):
		username = request.data.get('username')
		user = User.objects.filter(username=username).first()

		if not user:
			return Response({'error': _("Foydalanuvchi topilmadi!")}, status=status.HTTP_404_NOT_FOUND)
		
		if not request.user.is_superuser and user.is_superuser:
			return Response({'error': _(f"Bu amalga ruxsatingiz yetarli emas!")},status=status.HTTP_200_OK)
	
		if user.is_staff:
			user.is_staff=False
			user.save()
			return Response({'error': _(f"Foydalanuvchi {username} admin darajasidan tushurildi!")},status=status.HTTP_200_OK)
		
		user.is_staff = True
		user.save()

		return Response({'success': f"Foydalanuvchi {username} admin darajasiga ko'tarildi!"}, status=status.HTTP_200_OK)
	
