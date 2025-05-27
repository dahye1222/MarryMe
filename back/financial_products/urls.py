from django.urls import path
from . import views

urlpatterns = [
    # 예금상품조회
    path('deposits/', views.deposit_product_list),
    path('deposits/<int:product_id>/', views.deposit_product_detail),
    # 적금상품조회
    path('savings/', views.saving_product_list),
    path('savings/<int:product_id>/', views.saving_product_detail),
    # 대출상품조회
    path('loans/', views.loan_product_list),
    path('loans/<int:product_id>/', views.loan_product_detail),
    # 위시리스트(예적금 옵션 // 대출 상품)
    path('wishlist/deposit-option/<int:option_id>/toggle/', views.toggle_wishlist_deposit_option),
    path('wishlist/saving-option/<int:option_id>/toggle/', views.toggle_wishlist_saving_option),
    path('wishlist/loans/<int:loan_id>/toggle/', views.toggle_wishlist_loan),


]
