from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model  # 커스텀 User 모델 가져오기
from products.models import Product, ProductImage
import random
from django.http import JsonResponse

User = get_user_model()  # 현재 설정된 사용자 모델


def login(request):
    if request.user.is_authenticated:
       return redirect('accounts:profile', id=request.user.id) 
      

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('accounts:profile', id=request.user.id)   # 성공 시 GET 요청으로 리디렉션
        else:
            # 인증 실패 시 에러 메시지를 세션에 저장
            request.session['error_message'] = "Invalid username or password"
            return redirect("accounts:login")  # GET 요청으로 리디렉션

    # GET 요청일 때 세션에서 에러 메시지를 가져옴
    error_message = request.session.pop('error_message', None)
    return render(request, "accounts/login.html", {"error_message": error_message})


@login_required(login_url='accounts:login')
def logout(request):
    auth_logout(request)  # 세션 데이터를 삭제하고 사용자 로그아웃
    return redirect("accounts:login")  # 로그아웃 후 로그인 페이지로 리디렉션


def signup(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # 사용자 이름 중복 확인
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("accounts:signup")
        
        
        # 비밀번호 확인
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:signup")

        # 사용자 생성
        user = User.objects.create_user(
            username=username, password=password, first_name=full_name
        )
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("accounts:login")

    return render(request, "accounts/signup.html")



@login_required(login_url='accounts:login')
def profile(request, id):
    user = get_object_or_404(User, id=id)

    # 사용자가 등록한 상품 목록
    products = Product.objects.filter(user=user).prefetch_related('images')
    product_data = [
        {
            'product': product,
            'image': product.images.first().image.url if product.images.exists() else None
        }
        for product in products
    ]

    # 사용자의 위시리스트
    wishlist_items = Product.objects.filter(liked_users=user).prefetch_related('images')
    wishlist_data = [
        {
            'product': product,
            'image': product.images.first().image.url if product.images.exists() else None
        }
        for product in wishlist_items
    ]

    # 현재 사용자의 팔로우 여부 확인
    is_following = request.user.following.filter(id=user.id).exists()

    # 랜덤 사용자 추천
    users = User.objects.exclude(id=request.user.id)
    random_users = random.sample(list(users), min(len(users), 6))
    users_data = [
        {
            'id': random_user.id,
            'username': random_user.username,
            'first_name': random_user.first_name,
            'profile_image': random_user.profile_image.url if random_user.profile_image else None,
            'is_following': request.user.following.filter(id=random_user.id).exists()
        }
        for random_user in random_users
    ]

    context = {
        'user_profile': user,
        'product_data': product_data,
        'wishlist_data': wishlist_data,
        'is_owner': request.user == user,  # 내 프로필 여부 확인
        'is_following': is_following,  # 팔로우 여부
        'followers_count': user.followers.count(),  # 팔로워 수
        'following_count': user.following.count(),  # 팔로잉 수
        'users_data': users_data,  # 랜덤 사용자 목록
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.user != target_user:
        request.user.following.add(target_user)
        return JsonResponse({'status': 'followed'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def unfollow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.user != target_user:
        request.user.following.remove(target_user)
        return JsonResponse({'status': 'unfollowed'})
    return JsonResponse({'status': 'error'}, status=400)