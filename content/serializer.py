from rest_framework import serializers


class PageSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    pr_1 = serializers.CharField(required=False, allow_blank=True)
    pr_2 = serializers.CharField(required=False, allow_blank=True)
    pr_3 = serializers.CharField(required=False, allow_blank=True)
    img_1 = serializers.CharField(required=False, allow_blank=True)
    img_2 = serializers.CharField(required=False, allow_blank=True)
    img_3 = serializers.CharField(required=False, allow_blank=True)

