from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


# 🔹 Base Product Serializer (공통 필드 정의)
class BaseProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']

    def get_image(self, obj):
        return obj.images.first().image.url if obj.images.exists() else None


