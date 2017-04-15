from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from users import serializers

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_user(request, format=None):
    serializer = serializers.UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = serializers.UserSerializer(request.data)
        return Response({ 'user': user.data })
    else:
        return Response({ 'errors': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):

    def get(self, request, format=None):
        user = serializers.UserSerializer(request.user)
        return Response({ 'user': user.data })

    def put(self, request, format=None):
        serializer = serializers.UserCreateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user = serializers.UserSerializer(request.user)
            return Response({ 'user': user.data })
        else:
            return Response({ 'errors': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

