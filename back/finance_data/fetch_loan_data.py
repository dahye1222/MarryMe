import requests
from financial_products.models import LoanProduct, LoanOption
from django.conf import settings

API_KEY = settings.FIN_API_KEY

def fetch_and_save_loan_products():
    print("🔁 [전세대출 상품] API 호출 시작")
    url = "https://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json"
    params = {
        "auth": API_KEY,
        "topFinGrpNo": "020000",  # 은행권
        "pageNo": 1,
    }

    response = requests.get(url, params=params)
    data = response.json()["result"]

    base_list = data["baseList"]
    option_list = data["optionList"]

    for base in base_list:
        product, _ = LoanProduct.objects.update_or_create(
            fin_prdt_cd=base["fin_prdt_cd"],
            defaults={
                "fin_co_no": base["fin_co_no"],
                "kor_co_nm": base["kor_co_nm"],
                "fin_prdt_nm": base["fin_prdt_nm"],
                "join_way": base.get("join_way", ""),
                "loan_inci_expn": base.get("loan_inci_expn", ""),
                "erly_rpay_fee": base.get("erly_rpay_fee", ""),
                "dly_rate": base.get("dly_rate", ""),
                "loan_lmt": base.get("loan_lmt", "")
            }
        )


    for opt in option_list:
        product = LoanProduct.objects.filter(fin_prdt_cd=opt["fin_prdt_cd"]).first()
        if product:
            LoanOption.objects.create(
                loan_product=product,
                rpay_type=opt["rpay_type"],
                rpay_type_nm=opt["rpay_type_nm"],
                lend_rate_type=opt["lend_rate_type"],
                lend_rate_type_nm=opt["lend_rate_type_nm"],
                lend_rate_min=opt.get("lend_rate_min"),
                lend_rate_max=opt.get("lend_rate_max"),
                lend_rate_avg=opt.get("lend_rate_avg"),
            )

    print("✅ 전세대출 상품 저장 완료!")
