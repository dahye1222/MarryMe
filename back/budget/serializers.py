from rest_framework import serializers
from .models import WeddingBudget

class WeddingBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeddingBudget
        exclude = ['id', 'user', 'created_at']
        extra_kwargs = {field: {'required': False, 'allow_null': True} for field in model._meta.get_fields() if field.name not in ['id', 'user', 'created_at']}
