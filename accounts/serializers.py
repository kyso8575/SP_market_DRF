from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.models import Product

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