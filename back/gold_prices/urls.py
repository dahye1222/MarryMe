# gold_prices/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('metal-prices/', views.metal_price_list),
]
