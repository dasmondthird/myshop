# products/urls.py

from django.urls import path
from .views import product_list, product_detail

app_name = 'products'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('category/<slug:category_slug>/', product_list, name='product_list_by_category'),
    path('<slug:slug>/', product_detail, name='product_detail'),
]