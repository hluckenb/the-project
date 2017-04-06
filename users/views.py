from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from users import serializers

class UserView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        return Response({'detail': "Hello REST World"})

    def post(self, request, format=None):
        serializer = serializers.UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            del data['password']
            return Response({ 'success': 'true', 'user': data })
        else:
            return Response({ 'success': 'false', 'errors': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        return Response({})