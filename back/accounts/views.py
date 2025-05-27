from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer, UserUpdateSerializer


# 마이페이지 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

# 마이페이지 수정
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'gender': user.gender,
    })