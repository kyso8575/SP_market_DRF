from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='accounts:login')  # 로그인되지 않은 경우 리디렉션할 URL
def product_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("description")
        price = request.POST.get("price")
        condition = request.POST.get("condition")
    return render(request, "products/product_create.html")