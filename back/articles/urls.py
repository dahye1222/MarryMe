from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list_create),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.comment_list_create),
    path('comments/<int:comment_pk>/', views.comment_update_delete),
]
