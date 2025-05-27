import os
import sys
import django
import random

# Django 환경 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weddingProject.settings")
django.setup()

from accounts.models import User
from financial_products.models import DepositOption, SavingOption, LoanProduct


users = User.objects.all()
options = list(DepositOption.objects.select_related('deposit_product'))

for user in users:
    # 30% 확률로 옵션 1~3개 찜
    if random.random() < 0.3:
        selected = random.sample(options, min(len(options), random.randint(1, 3)))
        for opt in selected:
            user.wishlist_deposits_options.add(opt)

print("✅ 예금 옵션 위시리스트 더미 데이터 생성 완료!")

saving_options = list(SavingOption.objects.select_related('saving_product'))

for user in users:
    if random.random() < 0.3:
        selected = random.sample(saving_options, min(len(saving_options), random.randint(1, 3)))
        for opt in selected:
            user.wishlist_savings_options.add(opt)

print("✅ 적금 옵션 위시리스트 더미 데이터 생성 완료!")

# 전세 대출상품 위시리스트
loan_products = list(LoanProduct.objects.all())

for user in users:
    if random.random() < 0.3:
        selected = random.sample(loan_products, min(len(loan_products), random.randint(1, 3)))
        for product in selected:
            user.wishlist_loans.add(product)

print("✅ 전세대출 위시리스트 더미 데이터 생성 완료!")
