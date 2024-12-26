from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.models import Product, ProductImage

User = get_user_model()


# 🔹 Base Product Serializer (공통 필드 정의)
class BaseProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']

    def get_image(self, obj):
        return obj.images.first().image.url if obj.images.exists() else None


# 🔹 Product Image Serializer (이미지 목록 직렬화)
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']



# 🔹 Product Create Serializer (상품 생성)
class ProductCreateSerializer(BaseProductSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta(BaseProductSerializer.Meta):
        fields = BaseProductSerializer.Meta.fields + [
            'description', 'condition', 'images'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        user = self.context['request'].user
        
        # 상품 객체 생성
        product = Product.objects.create(user=user, **validated_data)
        
        # 이미지 객체 생성
        for image in images_data:
            ProductImage.objects.create(product=product, image=image)
        
        return product
    


class ProductLikeSerializer(serializers.ModelSerializer):
    """
    상품 좋아요 Serializer
    """
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'likes_count', 'is_liked']

    def get_is_liked(self, obj):
        """
        사용자가 이 상품을 좋아요 했는지 여부 반환
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_users.filter(id=request.user.id).exists()
        return False
    

class ProductEditSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    existing_images = ProductImageSerializer(many=True, read_only=True, source='images.all')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'condition', 'is_sold', 'images', 'existing_images']

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        
        # 상품 기본 정보 수정
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.is_sold = validated_data.get('is_sold', instance.is_sold)
        instance.save()
        
        # 이미지 추가
        for image in images_data:
            ProductImage.objects.create(product=instance, image=image)
        
        return instance