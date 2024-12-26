from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage
from django.contrib.auth import get_user_model  # 커스텀 User 모델 가져오기

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductCreateSerializer, BaseProductSerializer, ProductLikeSerializer, ProductEditSerializer

User = get_user_model()  # 현재 설정된 사용자 모델

# Create your views here.

class ProductCreateAPIView(APIView):
    """
    상품 생성 API
    """

    def post(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Product created successfully!",
                "product": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductListAPIView(APIView):
    """
    모든 상품 목록 API
    """
    def get(self, request):
        # 모든 상품을 최신순으로 가져오기
        products = Product.objects.all().order_by('-created_at')
        serializer = BaseProductSerializer(products, many=True, context={'request': request})
        return Response({
            "products": serializer.data
        }, status=status.HTTP_200_OK)




class ProductLikeAPIView(APIView):
    """
    상품 좋아요/취소 API
    """

    def post(self, request, product_id):
        """
        상품 좋아요/좋아요 취소
        """
        product = get_object_or_404(Product, id=product_id)
        
        if request.user in product.liked_users.all():
            product.liked_users.remove(request.user)
            product.likes_count -= 1
            status_text = 'unliked'
        else:
            product.liked_users.add(request.user)
            product.likes_count += 1
            status_text = 'liked'
        
        product.save()
        serializer = ProductLikeSerializer(product, context={'request': request})
        return Response({
            'status': status_text,
            'likes_count': product.likes_count,
            'product': serializer.data
        }, status=status.HTTP_200_OK)




class ProductEditAPIView(APIView):
    """
    상품 수정 API
    """

    def get(self, request, product_id):
        """
        상품 수정 정보 조회
        """
        product = get_object_or_404(Product, id=product_id, user=request.user)
        serializer = ProductEditSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        """
        상품 정보 수정
        """
        product = get_object_or_404(Product, id=product_id, user=request.user)
        serializer = ProductEditSerializer(product, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Product updated successfully!",
                "product": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteAPIView(APIView):
    """
    상품 삭제 API
    """

    def delete(self, request, product_id):
        """
        상품 삭제
        """
        product = get_object_or_404(Product, id=product_id)

        # 상품 소유자 확인
        if product.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this product."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        product.delete()
        return Response(
            {"detail": "Product deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )