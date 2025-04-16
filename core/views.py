from django.shortcuts import render
from .models import Product, Category, ProductImages

def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(product_status='published', featured=True)
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)

def product_list_view(request):
    # products = Product.objects.filter(product_status='published')
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'core/products.html', context)

def single_product_view(request, pid):
    try:
        product = Product.objects.get(pid=pid)
    except Product.DoesNotExist:
        product = None
        return render(request, 'core/404.html', {'product': product})
    
    product_images = ProductImages.objects.filter(product=product)
    
    context = {
        'product': product,
        'product_images': product_images
    }
    
    return render(request, 'core/single_product.html', context)
    
        
        

