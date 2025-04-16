from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list_view, name='product_list'),
    path('product/<str:pid>', views.single_product_view, name='product'),
]