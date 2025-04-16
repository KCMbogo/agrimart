from django.shortcuts import render
from .models import Product, Category, ProductImages, Vendor

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
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'core/products.html', context)

def single_product_view(request, pid):
    try:
        product = Product.objects.get(pid=pid)
    except Product.DoesNotExist:
        product = None
        return render(request, 'core/404.html', {'product': product})
    
    product_images = ProductImages.objects.filter(product=product)
    related_products = Product.objects.filter(vendor=product.vendor).exclude(pid=product.pid)[:4]
    
    context = {
        'product': product,
        'product_images': product_images,
        'related_products': related_products,
    }
    
    return render(request, 'core/single_product.html', context)
    
def vendor_list_view(request):
    vendors = Vendor.objects.all()
    count = vendors.count()
    
    context = {
        'vendors': vendors,
        'vendor_count':  count,
    }    
    
    return render(request, 'core/vendors.html', context)    

def single_vendor_view(request, vid):
    try:
        vendor = Vendor.objects.get(vid=vid)
    except Vendor.DoesNotExist:
        vendor = None
        return render(request, 'core/404.html', {'vendor': vendor})
    
    products = Product.objects.filter(vendor=vendor)
    
    context = {
        'products': products,
        'vendor': vendor
    }
    
    return render(request, 'core/single_vendor.html', context)