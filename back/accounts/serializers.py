from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User
from financial_products.models import DepositProduct, SavingProduct
from financial_products.serializers import (
    DepositOptionWithProductSerializer,
    SavingOptionWithProductSerializer,
    LoanListSerializer,
)

# dj-rest-auth를 이용한 회원가입 커스터마이징
class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(max_length=20)
    nickname = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=30, required=False, allow_blank=True, allow_null=True)
    birth_date = serializers.DateField(required=True, allow_null=False)
    GENDER_CHOICES = [
        ('M', '남성'),
        ('W', '여성'),
    ]
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES,
        allow_blank=True,
        allow_null=True
    )
    # 사용자가 이미지를 업로드하지 않을 때 사용할 기본 이미지 경로 설정
    profile_img = serializers.ImageField(required=False)
    salary = serializers.IntegerField(required=True, allow_null=False)
    wealth = serializers.IntegerField(required=True, allow_null=False)
    


    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['username'] = self.validated_data.get('username', '')
        data['nickname'] = self.validated_data.get('nickname', '')
        data['birth_date'] = self.validated_data.get('birth_date', None)
        data['gender'] = self.validated_data.get('gender', '')
        data['profile_img'] = self.validated_data.get('profile_img', None)
        data['salary'] = self.validated_data.get('salary', 0)
        data['wealth'] = self.validated_data.get('wealth', 0)
        return data
    
    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname')
        user.birth_date = self.validated_data.get('birth_date', None)
        user.gender = self.validated_data.get('gender')
        user.profile_img = self.validated_data.get('profile_img')
        user.salary = self.validated_data.get('salary')
        user.wealth = self.validated_data.get('wealth')
        user.save()
        return user





# 프로필페이지에 응답할 데이터 직렬화
class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    wishlist_deposits_options = DepositOptionWithProductSerializer(many=True, read_only=True)
    wishlist_savings_options = SavingOptionWithProductSerializer(many=True, read_only=True)
    wishlist_loans = LoanListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'nickname', 'birth_date', 'age', 'gender',
            'profile_img', 'salary', 'wealth',
            'wishlist_deposits_options', 'wishlist_savings_options', 'wishlist_loans',
        )

    def get_age(self, obj):
        from datetime import date
        if obj.birth_date:
            today = date.today()
            return today.year - obj.birth_date.year - (
                (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day)
            )
        return None

# 프로필페이지 수정 가능한 필드 정의
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'nickname', 'birth_date', 'gender',
            'profile_img', 'salary', 'wealth'
        ]