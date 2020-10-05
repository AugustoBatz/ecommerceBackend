from rest_framework import serializers
from user.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'address_a', 'address_b','email', 'is_admin', 'password', 'salt']
        extra_kwargs = {'password': {'write_only': True}, 'salt': {'write_only': True}}

class CustomSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, allow_blank=True, max_length=100)
    username = serializers.CharField(required=True, allow_blank=True, max_length=100)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True, max_length = 128)
    address_a = serializers.CharField(required=True)
    address_b = serializers.CharField()
    email = serializers.EmailField()
    is_admin = serializers.BooleanField(default=False)
    password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializerSignUp(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password', 'address_a', 'address_b', 'username', 'salt', 'phone')
        extra_kwargs = {'password': {'write_only': True}, 'salt': {'write_only': True}}

class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
