from user.models import User
from order.models import Basket

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

import re

def custom_validate_password(data):
    try:
        validate_password(data)
    except DjangoValidationError as e:
        raise ValidationError(
            {
                'password': e.messages
            }
        )
    return data

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
        pattern = r"^\+998(33|88|97|99|91|93|90|94|98|95|50|55|77|78)\d{7}$"
        if not re.match(pattern, value): 
            raise ValidationError(_(f"Ushbu {value} kantakt O'zbekistonga tegishli emas!"))
        return value

    def validate_email(self, value):
        user_exists = User.objects.filter(email=value).exists()
        if user_exists:
            raise ValidationError(_(f"Ushbu {value} email band!"))
        return value
    
    def validate_password(self, data):
        return custom_validate_password(data)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            username=validated_data['username']
        )
        Basket.objects.create(
            user = user
        )
        return user
    
class RegistrationBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

class UsernamePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)  
    username = serializers.CharField(allow_null=True)
    class Meta:
        model = User
        fields = ['password' ,'username', 'new_password'] 

    def validate_password1(self, value):
        print(f"Validating new_password: {value}")  
        return custom_validate_password(value)


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone'] 
        read_only_fields = fields