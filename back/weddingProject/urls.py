"""
URL configuration for weddingProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    #회원가입 및 로그인 관련 api
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    # 금융상품 관련 api
    path('api/products/', include('financial_products.urls')),
    # 상품 추천 api
    path('api/recommend/', include('recommend.urls')),
    # 프로필페이지 api
    path('api/accounts/', include('accounts.urls')),
    #게시판 api
    path('api/articles/', include('articles.urls')),
    #결혼비용계산기
    path('api/budget/', include('budget.urls')),
    path('api/gold-prices/', include('gold_prices.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

