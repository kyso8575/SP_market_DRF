from django.urls import path
from . import views


app_name = "products"
urlpatterns = [
    path("product_create/", views.product_create, name="product_create"),
]
