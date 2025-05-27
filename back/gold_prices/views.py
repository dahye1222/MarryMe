from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MetalPrice
from .serializers import MetalPriceSerializer

@api_view(['GET'])
def metal_price_list(request):
    metal = request.GET.get('metal')
    if metal not in ['gold', 'silver']:
        return Response({'error': 'metal 파라미터가 잘못되었습니다 (gold 또는 silver만 가능)'}, status=400)
    
    prices = MetalPrice.objects.filter(metal_type=metal).order_by('date')
    serializer = MetalPriceSerializer(prices, many=True)
    return Response(serializer.data)
