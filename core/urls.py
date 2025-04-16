from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list_view, name='product_list'),
    path('product/<str:pid>', views.single_product_view, name='product'),
    
    path('vendors/', views.vendor_list_view, name="vendor_list"),
    path('vendor/<str:vid>', views.single_vendor_view, name='vendor')
]