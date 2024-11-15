from user.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.tokens import RefreshToken
import re

class RefreshTokenSerializer(serializers.ModelSerializer):
    refresh_token = serializers.CharField()
    class Meta:
        model = User
        fields = ['refresh_token']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone', 'created_at', 'telegram_id', 'email']

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    username = serializers.CharField()

    def validate_phone(self, value):
        pattern = r"^(?:\+998(33|88|97|99|91|93)\d{7})$"
        if not re.match(pattern, value): 
            raise ValidationError(_(f"Ushbu {value} kantakt O'zbekistonga tegishli emas!"))
        return value

    def validate_email(self, value):
        user_exists = User.objects.filter(email=value).exists()
        if user_exists:
            raise ValidationError(_(f"Ushbu {value} email band!"))
        return value
    
    def validate_password(self, data):
        try:
            validate_password(data)
        except DjangoValidationError as e:
            raise ValidationError(
                {
                    'password': e.messages
                }
            )
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            username=validated_data['username']
        )
        refresh_token = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }
        
class RegistrationBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
