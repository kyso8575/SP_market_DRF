from django.urls import path
from . import views



app_name = "accounts"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("signup/", views.SignupAPIView.as_view(), name="signup"),
    path('profile/<int:id>/', views.UserProfileAPIView.as_view(), name='profile'),
    path('follow/<int:user_id>/', views.FollowUnfollowAPIView.as_view(), name='follow_user'),
]
