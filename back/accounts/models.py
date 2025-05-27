from django.db import models
from django.contrib.auth.models import AbstractUser
from financial_products.models import DepositOption, SavingOption, LoanProduct
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('M', '남성'),
        ('W', '여성'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    # 사용자가 이미지를 업로드하지 않을 때 사용할 기본 이미지 경로 설정
    profile_img = models.ImageField(upload_to='images/', default='images/default_profile.png')

    wishlist_deposits_options = models.ManyToManyField(DepositOption, blank=True, related_name='wishlisted_by_users')
    wishlist_savings_options = models.ManyToManyField(SavingOption, blank=True, related_name='wishlisted_by_users')
    wishlist_loans = models.ManyToManyField(LoanProduct, related_name='wishlisted_by_users', blank=True)
    salary = models.IntegerField(default=0)
    wealth = models.IntegerField(default=0)
