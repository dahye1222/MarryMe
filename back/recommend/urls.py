# recommend/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.recommend_deposit),
    path('saving/', views.recommend_saving),
    path('loans/', views.recommend_loans),
    
]
