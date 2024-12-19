# Create your models here.
from django.db import models
from django.conf import settings

# 사용자 모델 연결 (settings.AUTH_USER_MODEL)
User = settings.AUTH_USER_MODEL

class Product(models.Model):
    """상품 모델"""
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")  # 판매자
    name = models.CharField(max_length=255)  # 상품 이름
    description = models.TextField()  # 상품 설명
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 상품 가격
    condition = models.CharField(
        max_length=50,
        choices=[
            ('new', 'New'),
            ('like_new', 'Like New'),
            ('used', 'Used'),
        ],
        default='used',
    )  # 상품 상태
    images = models.ImageField(upload_to="product_images/")  # 상품 이미지
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간
    is_sold = models.BooleanField(default=False)  # 판매 여부

    def __str__(self):
        return self.name

class Favorite(models.Model):
    """찜 목록 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")  # 사용자
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorited_by")  # 찜한 상품
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    class Meta:
        unique_together = ('user', 'product')  # 사용자와 상품의 중복 방지

    def __str__(self):
        return f"{self.user.username} favorited {self.product.name}"
