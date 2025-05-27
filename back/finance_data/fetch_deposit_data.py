# finance_data/fetch_deposit_data.py

import requests
from financial_products.models import DepositProduct, DepositOption
from django.conf import settings

API_KEY = settings.FIN_API_KEY  # settings.py에 FIN_API_KEY 정의 필요

def fetch_and_save_deposit_products():
    print("👉 [예금 상품 정보] API 호출 시작")

    url = "https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    params = {
        "auth": API_KEY,
        "topFinGrpNo": "020000",  # 은행
        "pageNo": 1,
    }

    response = requests.get(url, params=params)
    data = response.json()

    base_list = data['result']['baseList']      # 상품 기본 정보
    option_list = data['result']['optionList']  # 옵션 정보 (금리 등)

    # 기존 데이터 모두 삭제 (전체 갱신 방식)
    DepositProduct.objects.all().delete()

    for base in base_list:
        product = DepositProduct.objects.create(
            dcls_month=base['dcls_month'],
            fin_prdt_cd=base['fin_prdt_cd'],
            fin_co_no=base['fin_co_no'],
            kor_co_nm=base['kor_co_nm'],
            fin_prdt_nm=base['fin_prdt_nm'],
            join_way=base['join_way'],
            mtrt_int=base['mtrt_int'],
            spcl_cnd=base['spcl_cnd'],
            join_deny=int(base['join_deny']),
            join_member=base['join_member'],
            etc_note=base['etc_note'],
            max_limit=int(base['max_limit']) if base.get('max_limit') else None
        )

        # 이 상품에 대한 옵션 필터링해서 저장
        for option in filter(lambda x: x['fin_prdt_cd'] == product.fin_prdt_cd, option_list):
            DepositOption.objects.create(
                deposit_product=product,
                intr_rate_type=option['intr_rate_type'],
                intr_rate_type_nm=option['intr_rate_type_nm'],
                save_trm=int(option['save_trm']),
                intr_rate=float(option['intr_rate']) if option['intr_rate'] else None,
                intr_rate2=float(option['intr_rate2']) if option['intr_rate2'] else None
            )

    print("✅ 예금 상품 저장 완료")
