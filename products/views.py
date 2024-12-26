from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, ProductImage
from django.contrib.auth import get_user_model  # 커스텀 User 모델 가져오기
from django.http import JsonResponse

User = get_user_model()  # 현재 설정된 사용자 모델

# Create your views here.

@login_required(login_url='accounts:login')  # 로그인하지 않은 경우 로그인 페이지로 리디렉션
def product_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        condition = request.POST.get("condition")
        images = request.FILES.getlist("images")  # 여러 이미지 받기

        # 필수 필드 검증
        if not all([name, description, price, condition]):
            return render(request, "products/product_create.html", {
                "error": "All fields are required"
            })

        # Product 객체 생성 및 저장
        product = Product.objects.create(
            user=request.user,
            name=name,
            description=description,
            price=price,
            condition=condition
        )

        # 여러 이미지 저장
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('accounts:profile', id=request.user.id) 

    return render(request, "products/product_create.html")



def product_list(request):
    # 모든 상품을 최신순으로 가져오기
    products = Product.objects.all().order_by('-created_at')

    # 각 상품에 대한 첫 번째 이미지 포함
    product_data = []
    for product in products:
        first_image = ProductImage.objects.filter(product=product).first()
        product_data.append({
            'product': product,
            'image': first_image.image.url if first_image else None  # 첫 번째 이미지 URL 또는 None
        })
    
    # 컨텍스트에 상품 데이터 전달
    context = {
        'product_data': product_data,  # 상품 + 첫 번째 이미지
    }

    return render(request, 'products/product_list.html', context)




@login_required(login_url='accounts:login')
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user in product.liked_users.all():
        product.liked_users.remove(request.user)
        product.likes_count -= 1
        status = 'unliked'
    else:
        product.liked_users.add(request.user)
        product.likes_count += 1
        status = 'liked'
    
    product.save()
    
    return JsonResponse({'status': status, 'likes_count': product.likes_count})



def product_detail(request, product_id):
    # 상품 객체 가져오기
    product = get_object_or_404(Product, id=product_id)
    
    # 해당 상품의 이미지 목록 가져오기
    product_images = ProductImage.objects.filter(product=product)
    
    # 좋아요 여부 확인
    is_liked = request.user in product.liked_users.all() if request.user.is_authenticated else False
    
    context = {
        'product': product,
        'product_images': product_images,
        'is_liked': is_liked,
    }
    
    return render(request, 'products/product_detail.html', context)

def product_edit(request, product_id):
    # 상품 객체 가져오기
    product = get_object_or_404(Product, id=product_id)
    product_images = ProductImage.objects.filter(product=product)

    if request.method == 'POST':
        # 상품 정보 수정
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.condition = request.POST['condition']
        product.is_sold = 'is_sold' in request.POST
        
        # 이미지 업로드
        if 'images' in request.FILES:
            for img in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=img)

        product.save()

        return redirect('accounts:profile', id=request.user.id)

    # GET 요청: 기존 정보 채우기
    context = {
        'product': product,
        'product_images': product_images
    }
    return render(request, 'products/product_edit.html', context)


def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('accounts:profile', id=request.id)