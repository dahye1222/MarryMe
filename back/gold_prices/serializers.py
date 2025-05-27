from rest_framework import serializers
from .models import MetalPrice

class MetalPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetalPrice
        fields = ['metal_type', 'date', 'close_price', 'high_price', 'low_price']
