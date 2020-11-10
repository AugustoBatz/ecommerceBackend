from rest_framework import serializers



class SerializerContact(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=True, max_length=100)
    useremail = serializers.CharField(required=True, allow_blank=True, max_length=100)
    asunt = serializers.CharField(required=True, allow_blank=True, max_length=100)
    message = serializers.CharField(required=True, allow_blank=True, max_length=1000)



