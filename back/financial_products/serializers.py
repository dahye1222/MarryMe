from rest_framework import serializers
from .models import DepositProduct, SavingProduct, DepositOption, SavingOption, LoanProduct, LoanOption
from accounts.models import User

# 예금 상품(옵션) 마이페이지에서 뿌릴 때 데이터 직렬화
class WishlistDepositSerializer(serializers.ModelSerializer):
    fin_prdt_nm = serializers.CharField(source='deposit_product.fin_prdt_nm', read_only=True)
    kor_co_nm = serializers.CharField(source='deposit_product.kor_co_nm', read_only=True)

    class Meta:
        model = DepositOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2', 'intr_rate_type_nm', 'fin_prdt_nm', 'kor_co_nm']

# 적금 상품(옵션) 마이페이지에서 뿌릴 때 데이터 직렬화
class WishlistSavingSerializer(serializers.ModelSerializer):
    fin_prdt_nm = serializers.CharField(source='saving_product.fin_prdt_nm', read_only=True)
    kor_co_nm = serializers.CharField(source='saving_product.kor_co_nm', read_only=True)

    class Meta:
        model = SavingOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2', 'intr_rate_type_nm', 'fin_prdt_nm', 'kor_co_nm']

# 대출 상품 마이페이지에서 뿌릴 때 데이터 직렬화
class LoanListSerializer(serializers.ModelSerializer):
    min_lend_rate = serializers.SerializerMethodField()

    class Meta:
        model = LoanProduct
        fields = [
            'id',
            'fin_prdt_cd',
            'kor_co_nm',
            'fin_prdt_nm',
            'loan_lmt',
            'min_lend_rate',  #최소 금리 추가
        ]

    def get_min_lend_rate(self, obj):
        options = obj.options.all()
        min_rate = min(
            [opt.lend_rate_min for opt in options if opt.lend_rate_min is not None],
            default=None
        )
        return round(min_rate, 2) if min_rate is not None else None


# 예금상품 Option data 직렬화
class DepositOptionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2']

# 예금상품 전체 조회 시 직렬화
class DepositProductListSerializer(serializers.ModelSerializer):
    options = DepositOptionSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProduct
        fields = ['id', 'kor_co_nm', 'fin_prdt_nm', 'options']


# 예금상품 상세 정보시 필요한 데이터
class DepositProductDetailSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='kor_co_nm')
    product_name = serializers.CharField(source='fin_prdt_nm')

    class Meta:
        model = DepositProduct
        fields = [
            'id',
            'bank_name',
            'product_name',
            'dcls_month',
            'join_way',
            'mtrt_int',
            'spcl_cnd',
            'join_member',
            'join_deny',
            'max_limit',
            'etc_note',
        ]


# 적금상품 Option data 직렬화
class SavingOptionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2']

# 적금상품 전체 조회 시 직렬화
class SavingProductListSerializer(serializers.ModelSerializer):
    options = SavingOptionSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = SavingProduct
        fields = ['id', 'kor_co_nm', 'fin_prdt_nm', 'options']

        
# 적금상품 상세 정보시 필요한 데이터
class SavingProductDetailSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='kor_co_nm')
    product_name = serializers.CharField(source='fin_prdt_nm')

    class Meta:
        model = SavingProduct
        fields = [
            'id',
            'bank_name',
            'product_name',
            'dcls_month',
            'join_way',
            'mtrt_int',
            'spcl_cnd',
            'join_member',
            'join_deny',
            'max_limit',
            'etc_note',
        ]

# 대출 상품 상세페이지에 뿌릴 데이터 직렬화화
class LoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOption
        fields = [
            'id', 'rpay_type', 'rpay_type_nm',
            'lend_rate_type', 'lend_rate_type_nm',
            'lend_rate_min', 'lend_rate_max', 'lend_rate_avg'
        ]

class LoanDetailSerializer(serializers.ModelSerializer):
    options = LoanOptionSerializer(many=True, read_only=True)

    class Meta:
        model = LoanProduct
        fields = [
            'id', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm',
            'join_way', 'loan_inci_expn', 'erly_rpay_fee',
            'dly_rate', 'loan_lmt', 'options'
        ]




# 찜한 예금 옵션 목록 조회용
class DepositProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = ['id', 'kor_co_nm', 'fin_prdt_nm']  # 은행명, 상품명만 간단히

class DepositOptionWithProductSerializer(serializers.ModelSerializer):
    deposit_product = DepositProductSimpleSerializer(read_only=True)

    class Meta:
        model = DepositOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2', 'deposit_product']

# 찜한 적금 옵션 목록 조회용
class SavingProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProduct
        fields = ['id', 'kor_co_nm', 'fin_prdt_nm']

class SavingOptionWithProductSerializer(serializers.ModelSerializer):
    saving_product = SavingProductSimpleSerializer(read_only=True)

    class Meta:
        model = SavingOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2', 'saving_product']




class DepositOptionRecommendSerializer(serializers.ModelSerializer):
    fin_prdt_nm = serializers.CharField(source='deposit_product.fin_prdt_nm')
    kor_co_nm = serializers.CharField(source='deposit_product.kor_co_nm')

    class Meta:
        model = DepositOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2', 'fin_prdt_nm', 'kor_co_nm']


class SavingOptionRecommendSerializer(serializers.ModelSerializer):
    fin_prdt_nm = serializers.CharField(source='saving_product.fin_prdt_nm')
    kor_co_nm = serializers.CharField(source='saving_product.kor_co_nm')

    class Meta:
        model = SavingOption
        fields = ['id', 'save_trm', 'intr_rate', 'intr_rate2', 'fin_prdt_nm', 'kor_co_nm']