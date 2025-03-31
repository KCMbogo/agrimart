from django.shortcuts import render
from .models import Product, Category

def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(product_status='published', featured=True)
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)

def product_list_view(request):
    products = Product.objects.filter(product_status='published')
    context = {
        'products': products,
    }
    return render(request, 'core/products.html', context)

