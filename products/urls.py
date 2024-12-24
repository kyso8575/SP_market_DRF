from django.urls import path
from . import views


app_name = "products"
urlpatterns = [
    path("product_create/", views.product_create, name="product_create"),
    path("product_list/", views.product_list, name="product_list"),
    path('like/<int:product_id>/', views.like_product, name='like_product'),
    path('product_detail/<int:product_id>', views.product_detail, name='product_detail'),
]
