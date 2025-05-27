from django.db import models

# Create your models here.

# 예금 모델
class DepositProduct(models.Model):
    dcls_month = models.TextField() # 공시 제출월
    fin_prdt_cd = models.TextField() # 금융상품 코드
    fin_co_no = models.TextField()  # 금융회사 코드
    kor_co_nm = models.TextField()  # 금융회사 명
    fin_prdt_nm = models.TextField() # 금융상품 명
    join_way = models.TextField() # 가입방법
    mtrt_int = models.TextField() # 만기 후 이자율
    spcl_cnd = models.TextField() # 우대조건
    join_deny = models.IntegerField(default=0) # 가입제한
    join_member = models.TextField() #가입대상
    etc_note = models.TextField() # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True) # 최고한도

class DepositOption(models.Model):
    # fin_prdt_cd = models.IntegerField()
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options') # 예금상품 참조
    intr_rate_type = models.CharField(max_length=100) # 예금 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100) # 예금 금리 유형명    
    save_trm = models.IntegerField(default=0) # 예치기간
    intr_rate = models.FloatField(null=True) # 저축 금리
    intr_rate2 = models.FloatField(null=True) # 최고 우대금리

# 적금 모델
class SavingProduct(models.Model):
    dcls_month = models.TextField() # 공시 제출월 
    fin_prdt_cd = models.TextField() # 금융회사 코드
    fin_co_no = models.TextField() # 금융회사 코드
    kor_co_nm = models.TextField() # 금융회사 명
    fin_prdt_nm = models.TextField() # 금융상품 명
    join_way = models.TextField() #가입방법
    mtrt_int = models.TextField() # 만기 후 이자율
    spcl_cnd = models.TextField() # 우대조건
    join_deny = models.IntegerField(default=0) #가입제한
    join_member = models.TextField() # 가입대상
    etc_note = models.TextField() # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True) # 최고한도도


class SavingOption(models.Model):
    # fin_prdt_cd = models.IntegerField()
    saving_product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, related_name='options') # 적금상품 참조
    intr_rate_type = models.CharField(max_length=100) # 적금 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100) # 적금 금리 유형명
    rsrv_type = models.TextField() # 적립 유형
    rsrv_type_nm = models.TextField() # 적립 유형명
    save_trm = models.IntegerField() # 저축기간
    intr_rate = models.FloatField(null=True) #적금 금리
    intr_rate2 = models.FloatField(null=True) # 최고 우대금리

# 대출 모델
class LoanProduct(models.Model):
    fin_prdt_cd = models.CharField(max_length=100, unique=True) # 금융상품 코드
    fin_co_no = models.CharField(max_length=100) # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100) # 금융회사 이름
    fin_prdt_nm = models.CharField(max_length=100) # 금융상품 이름
    join_way = models.TextField(null=True, blank=True) # 가입방법
    loan_inci_expn = models.TextField(null=True, blank=True) # 대출 부대비용
    erly_rpay_fee = models.TextField(null=True, blank=True) #중도상환 수수료
    dly_rate = models.TextField(null=True, blank=True) # 연체 이자율
    loan_lmt = models.TextField(null=True, blank=True) # 대출한도도


class LoanOption(models.Model):
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE, related_name='options')
    rpay_type = models.CharField(max_length=100) # 상환방식 코드
    rpay_type_nm = models.CharField(max_length=100) # 상환방식명
    lend_rate_type = models.CharField(max_length=100) # 대출금리유형 코드
    lend_rate_type_nm = models.CharField(max_length=100) # 대출금리유형
    lend_rate_min = models.FloatField(null=True) # 대출금리 최저
    lend_rate_max = models.FloatField(null=True) # 대출금리 최고
    lend_rate_avg = models.FloatField(null=True) # 전월 취급 평균금리
 