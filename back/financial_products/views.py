from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import DepositProduct, SavingProduct, DepositOption, SavingOption, LoanProduct
from accounts.models import User
from .serializers import DepositProductListSerializer, SavingProductListSerializer, DepositProductDetailSerializer, SavingProductDetailSerializer
from .serializers import WishlistDepositSerializer, WishlistSavingSerializer, LoanListSerializer, LoanDetailSerializer
from django.shortcuts import get_object_or_404
from .utils import (
    calculate_equal_installment,
    calculate_equal_principal,
    calculate_maturity_lump_sum,
)

# 예금 상품 전체 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def deposit_product_list(request):
    products = DepositProduct.objects.prefetch_related('options').all()
    serializer = DepositProductListSerializer(products, many=True)
    return Response(serializer.data)


# 적금 상품 전체 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def saving_product_list(request):
    products = SavingProduct.objects.prefetch_related('options').all()
    serializer = SavingProductListSerializer(products, many=True)
    return Response(serializer.data)

# 대출 상품 전체 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def loan_product_list(request):
    products = LoanProduct.objects.prefetch_related('options').all()
    serializer = LoanListSerializer(products, many=True)
    return Response(serializer.data)

# 예금 상세 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def deposit_product_detail(request, product_id):
    try:
        product = DepositProduct.objects.get(id=product_id)
    except DepositProduct.DoesNotExist:
        return Response({'error': '상품이 존재하지 않습니다.'}, status=404)

    serializer = DepositProductDetailSerializer(product)
    return Response(serializer.data)


# 적금 상품 상세 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def saving_product_detail(request, product_id):
    try:
        product = SavingProduct.objects.get(id=product_id)
    except SavingProduct.DoesNotExist:
        return Response({'error': '상품이 존재하지 않습니다.'}, status=404)

    serializer = SavingProductDetailSerializer(product)
    return Response(serializer.data)

# 대출 상품 상세 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def loan_product_detail(request, product_id):
    try:
        product = LoanProduct.objects.get(id=product_id)
    except LoanProduct.DoesNotExist:
        return Response({'error': '해당 대출상품이 존재하지 않습니다.'}, status=404)
    loan_amount = request.query_params.get('loan_amount')
    months = request.query_params.get('months')
    simulation_results = []

    if loan_amount and months:
        try:
            loan_amount = int(loan_amount)
            months = int(months)
        except ValueError:
            return Response({'error': 'loan_amount와 months는 정수여야 합니다.'}, status=400)

        for opt in product.options.all():
            rate = opt.lend_rate_avg or opt.lend_rate_min
            if rate is None:
                continue

            rpay_type = opt.rpay_type_nm.strip()

            if rpay_type in ["분할상환방식", "원리금균등"]:
                total, principal, interest = calculate_equal_installment(loan_amount, rate, months)
            elif rpay_type == "원금균등":
                total, principal, interest = calculate_equal_principal(loan_amount, rate, months)
            elif rpay_type == "만기일시상환방식":
                total, principal, interest = calculate_maturity_lump_sum(loan_amount, rate, months)
            else:
                continue

            simulation_results.append({
                "option_id": opt.id,
                "rpay_type_nm": opt.rpay_type_nm,
                "lend_rate_avg": rate,
                "총 상환금액": total,
                "원금": principal,
                "총 이자": interest
            })

    serializer = LoanDetailSerializer(product)
    return Response({
        "product": serializer.data,
        "repayment_simulation": simulation_results
    })

# 예금상품 위시리스트 담을 때 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_wishlist_deposit_option(request, option_id):
    user = request.user
    try:
        option = DepositOption.objects.get(id=option_id)
    except DepositOption.DoesNotExist:
        return Response({'error': '존재하지 않는 예금 옵션입니다.'}, status=404)

    if option in user.wishlist_deposits_options.all():
        user.wishlist_deposits_options.remove(option)
        return Response({'message': '예금 옵션 찜 해제 완료'})
    else:
        user.wishlist_deposits_options.add(option)
        return Response({'message': '예금 옵션 찜 등록 완료'})

# 적금 상품 위시리스트 담을 때 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_wishlist_saving_option(request, option_id):
    user = request.user
    try:
        option = SavingOption.objects.get(id=option_id)
    except SavingOption.DoesNotExist:
        return Response({'error': '존재하지 않는 적금 옵션입니다.'}, status=404)

    if option in user.wishlist_savings_options.all():
        user.wishlist_savings_options.remove(option)
        return Response({'message': '적금 옵션 찜 해제 완료'})
    else:
        user.wishlist_savings_options.add(option)
        return Response({'message': '적금 옵션 찜 등록 완료'})

# 대출 상품 위시리스트 담을 때 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_wishlist_loan(request, loan_id):
    user = request.user
    try:
        product = LoanProduct.objects.get(id=loan_id)
    except LoanProduct.DoesNotExist:
        return Response({'error': '존재하지 않는 대출 상품입니다.'}, status=404)

    if product in user.wishlist_loans.all():
        user.wishlist_loans.remove(product)
        return Response({'message': '대출 상품 찜 해제 완료'})
    else:
        user.wishlist_loans.add(product)
        return Response({'message': '대출 상품 찜 등록 완료'})
