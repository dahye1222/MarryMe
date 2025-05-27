import json
from pathlib import Path
from gold_prices.models import MetalPrice

def load_price_data(metal, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for row in data:
        MetalPrice.objects.update_or_create(
            metal_type=metal,
            date=row['Date'],
            defaults={
                'close_price': row['Close/Last'],
                'high_price': row['High'],
                'low_price': row['Low'],
            }
        )
