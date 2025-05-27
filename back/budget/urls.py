from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_budget_view),
    path('chat/', views.chat_with_budget_bot),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
