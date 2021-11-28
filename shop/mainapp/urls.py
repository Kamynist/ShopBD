from django.urls import path
from .views import test_v, shop, ProductDetailView

urlpatterns = [
    path('', test_v, name='base'),
    path('shop/', shop, name='shop'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name="product_detail")
]
