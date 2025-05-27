import json
from django.core.management.base import BaseCommand
from gold_prices.models import MetalPrice
from pathlib import Path


class Command(BaseCommand):
    help = 'Import gold and silver price data from JSON files'

    def handle(self, *args, **options):
        base_dir = Path('back/static/data')  # 파일 경로

        for metal in ['gold', 'silver']:
            file_path = base_dir / f"{metal}_prices.json"
            if not file_path.exists():
                self.stdout.write(self.style.ERROR(f"{file_path} 파일이 존재하지 않습니다."))
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            count = 0
            for row in data:
                _, created = MetalPrice.objects.update_or_create(
                    metal_type=metal,
                    date=row['Date'],
                    defaults={
                        'close_price': row['Close/Last'],
                        'high_price': row['High'],
                        'low_price': row['Low'],
                    }
                )
                if created:
                    count += 1

            self.stdout.write(self.style.SUCCESS(f"{metal} 데이터 {count}개 저장 완료 ✅"))
