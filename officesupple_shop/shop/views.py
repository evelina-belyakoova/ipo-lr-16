from django.shortcuts import render

def index(request):
    return render(request, 'shop/index.html')

def about(request):
    return render(request, 'shop/about.html')

def shop_info(request):
    return render(request, 'shop/shop_info.html')
