from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils import recommend_deposit_options, recommend_saving_options, recommend_loan_products
from financial_products.serializers import DepositOptionRecommendSerializer, LoanListSerializer, SavingOptionRecommendSerializer

# 예금 추천
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_deposit(request):
    options = recommend_deposit_options(request.user)
    serializer = DepositOptionRecommendSerializer(options, many=True)
    return Response(serializer.data)

# 적금 추천
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_saving(request):
    options = recommend_saving_options(request.user)
    serializer = SavingOptionRecommendSerializer(options, many=True)
    return Response(serializer.data)

# 대출 추천
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_loans(request):
    user = request.user
    recommended = recommend_loan_products(user)
    serializer = LoanListSerializer(recommended, many=True)
    return Response(serializer.data)