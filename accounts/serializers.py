from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.serializers import BaseProductSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_image', 'bio', 'following', 'followers']
        read_only_fields = ['following', 'followers']


class FollowSerializer(serializers.ModelSerializer):
    """
    팔로우 상태를 직렬화
    """
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'is_following']

    def get_is_following(self, obj):
        request_user = self.context.get('request').user
        return request_user.following.filter(id=obj.id).exists()
    


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
    