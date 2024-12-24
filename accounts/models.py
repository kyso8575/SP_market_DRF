from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """커스텀 사용자 모델"""
    
    # 📸 프로필 이미지 필드
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        default='profile_images/default_profile.png'
    )
    
    # 👥 팔로우 관계 필드
    following = models.ManyToManyField(
        'self',                # 같은 User 모델을 참조
        symmetrical=False,     # 비대칭 관계 (팔로우와 팔로워는 다름)
        related_name='followers',  # 역참조: 나를 팔로우하는 사용자들
        blank=True
    )

    # 👤 사용자 설명 필드 (선택 사항)
    bio = models.TextField(null=True, blank=True, max_length=500)

    def follow(self, user):
        """사용자를 팔로우"""
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        """사용자를 언팔로우"""
        if user != self:
            self.following.remove(user)

    def is_following(self, user):
        """특정 사용자를 팔로우 중인지 확인"""
        return self.following.filter(id=user.id).exists()

    def is_followed_by(self, user):
        """특정 사용자가 나를 팔로우 중인지 확인"""
        return self.followers.filter(id=user.id).exists()

    def __str__(self):
        return self.username
