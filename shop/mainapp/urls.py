from django.urls import path
from .views import test_v, shop

urlpatterns = [
    path('', test_v, name='base'),
    path('shop/', shop, name='shop'),
]
