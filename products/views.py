from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='accounts:login')  # 로그인되지 않은 경우 리디렉션할 URL
def product_create(request):
    return render(request, "products/product_create.html")