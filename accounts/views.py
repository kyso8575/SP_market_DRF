from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model  # 커스텀 User 모델 가져오기
from products.models import Product, ProductImage

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


@login_required(login_url='accounts:login')  # 로그인되지 않은 경우 리디렉션할 URL
def profile(request, id):

    # 1️⃣ 사용자 정보 가져오기
    user = get_object_or_404(User, id=id)
    
    # 2️⃣ 해당 사용자가 등록한 상품 가져오기
    products = Product.objects.filter(user=user)
    
    # 3️⃣ 각 상품의 첫 번째 이미지 가져오기
    product_data = []
    for product in products:
        first_image = ProductImage.objects.filter(product=product).first()
        product_data.append({
            'product': product,
            'image': first_image.image.url if first_image else None  # 첫 번째 이미지 URL 또는 None
        })

    context = {
        'user': user,          # 사용자 정보
        'product_data': product_data,  # 상품 + 첫 번째 이미지
    }

    return render(request, 'accounts/profile.html', context)

