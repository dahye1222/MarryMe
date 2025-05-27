from django.db import models
from accounts.models import User
# Create your models here.

class WeddingBudget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 상견례
    meal = models.PositiveIntegerField(null=True, blank=True)         # 식사
    gift = models.PositiveIntegerField(null=True, blank=True)         # 선물

    # 스드메
    studio_dress_makeup = models.PositiveIntegerField(null=True, blank=True)  # 스드메

    # 예식장
    hall = models.PositiveIntegerField(null=True, blank=True)         # 대관/식대
    mc = models.PositiveIntegerField(null=True, blank=True)           # 사회자
    officiant = models.PositiveIntegerField(null=True, blank=True)    # 주례
    congratulator = models.PositiveIntegerField(null=True, blank=True) # 축가
    bag_helper = models.PositiveIntegerField(null=True, blank=True)   # 가방순이
    snap_dvd = models.PositiveIntegerField(null=True, blank=True)     # 본식 스냅/DVD
    flower_shower = models.PositiveIntegerField(null=True, blank=True) # 플라워 샤워
    floral_decor = models.PositiveIntegerField(null=True, blank=True) # 꽃장식
    wedding_cake = models.PositiveIntegerField(null=True, blank=True) # 웨딩 케이크
    live_music = models.PositiveIntegerField(null=True, blank=True)   # 음악 연주
    pyebaek = models.PositiveIntegerField(null=True, blank=True)      # 폐백/이바지
    pre_wedding_video = models.PositiveIntegerField(null=True, blank=True) # 식전 영상
    bouquet = models.PositiveIntegerField(null=True, blank=True)      # 부케
    photo_table = models.PositiveIntegerField(null=True, blank=True)  # 포토테이블
    wedding_car = models.PositiveIntegerField(null=True, blank=True)  # 웨딩카

    # 신혼여행
    honeymoon = models.PositiveIntegerField(null=True, blank=True)    # 신혼여행

    created_at = models.DateTimeField(auto_now_add=True)
