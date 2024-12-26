from django.urls import path
from . import views


app_name = "products"
urlpatterns = [
    path("product_create/", views.ProductCreateAPIView.as_view(), name="product_create"),
    path("product_list/", views.ProductListAPIView.as_view(), name="product_list"),
    path('product_like/<int:product_id>/', views.ProductLikeAPIView.as_view(), name='like_product'),
    path('product_detail/<int:product_id>/', views.ProductDeleteAPIView.as_view(), name='product_detail'),
    path('product_edit/<int:product_id>/', views.ProductEditAPIView.as_view(), name='product_edit'),
    path('product_delete/<int:product_id>/', views.ProductDeleteAPIView.as_view(), name='product_delete'),
]
