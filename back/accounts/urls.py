from django.urls import path
from . import views

urlpatterns = [
    path('mypage/', views.my_profile),
    path('mypage/update/', views.update_profile),
    path('user/', views.current_user),
]
