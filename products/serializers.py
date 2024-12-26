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


# 🔹 Profile Product Serializer (사용자 상품 정보)
class ProfileProductSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        fields = BaseProductSerializer.Meta.fields + ['description']


# 🔹 User Profile Serializer (사용자 정보 + 상품 목록)
class UserProfileSerializer(serializers.ModelSerializer):
    products = ProfileProductSerializer(many=True, read_only=True, source='product_set')
    wishlist = BaseProductSerializer(many=True, read_only=True, source='liked_products')
    profile_image = serializers.SerializerMethodField()
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'profile_image', 'followers_count',
            'following_count', 'is_following', 'products', 'wishlist'
        ]

    def get_profile_image(self, obj):
        return obj.profile_image.url if obj.profile_image else None

    def get_is_following(self, obj):
        request_user = self.context.get('request').user
        return request_user.following.filter(id=obj.id).exists()


# 🔹 랜덤 사용자 추천 Serializer
class RandomUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'profile_image', 'is_following']

    def get_profile_image(self, obj):
        return obj.profile_image.url if obj.profile_image else None

    def get_is_following(self, obj):
        request_user = self.context.get('request').user
        return request_user.following.filter(id=obj.id).exists()
