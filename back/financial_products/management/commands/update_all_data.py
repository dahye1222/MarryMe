from django.core.management.base import BaseCommand
from finance_data.fetch_deposit_data import fetch_and_save_deposit_products
from finance_data.fetch_saving_data import fetch_and_save_saving_products
from finance_data.fetch_loan_data import fetch_and_save_loan_products
class Command(BaseCommand):
    help = "예금 + 적금 상품 정보를 외부 API에서 받아와 DB에 저장"

    def handle(self, *args, **kwargs):
        fetch_and_save_deposit_products()
        fetch_and_save_saving_products()
        fetch_and_save_loan_products()
        self.stdout.write(self.style.SUCCESS("✅ 모든 금융 상품 데이터 갱신 완료"))
