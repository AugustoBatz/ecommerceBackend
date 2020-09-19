from rest_framework import serializers
from user.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name', 'phone', 'address_a', 'address_b','email', 'is_admin', 'password', 'salt']

class CustomSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=True, max_length=100)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True, max_length = 128)
    address_a = serializers.CharField(required=True)
    address_b = serializers.CharField()
    email = serializers.EmailField()
    is_admin = serializers.BooleanField(default=False)
    password = serializers.CharField()


