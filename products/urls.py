from django.urls import path
from . import views


app_name = "products"
urlpatterns = [
    path("login/", views.login, name="login"),
]
