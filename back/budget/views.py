from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import WeddingBudget
from .serializers import WeddingBudgetSerializer

import openai
from django.conf import settings


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def my_budget_view(request):
    user = request.user
    try:
        budget = WeddingBudget.objects.get(user=user)
    except WeddingBudget.DoesNotExist:
        budget = WeddingBudget.objects.create(user=user)

    if request.method == 'GET':
        serializer = WeddingBudgetSerializer(budget)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = WeddingBudgetSerializer(budget, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 챗봇 기능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_budget_bot(request):
    user = request.user
    question = request.data.get('question')

    if not question:
        return Response({'error': '질문을 입력해주세요.'}, status=400)

    # 예산 자동 생성 또는 가져오기
    budget, _ = WeddingBudget.objects.get_or_create(user=user)

    # 예산 정보 구성
    filled_fields = [
        f"{field.verbose_name or field.name}: {getattr(budget, field.name)}원"
        for field in budget._meta.fields
        if field.name not in ['id', 'user', 'created_at']
        and getattr(budget, field.name) is not None
    ]
    budget_info = "\n".join(filled_fields) or "아직 입력된 예산 항목이 없습니다."

    # 프롬프트 구성
    prompt = f"""
    다음은 사용자의 결혼 예산 정보입니다:
    {budget_info}

    사용자의 질문: "{question}"

    이 정보를 바탕으로 간단하고 실용적인 조언을 200자 내외로 제공해줘.
    """

    # OpenAI 호출
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 결혼 준비 예산 전문가야."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        answer = response.choices[0].message.content
        return Response({'answer': answer})
    except Exception as e:
        return Response({'error': str(e)}, status=500)