from rest_framework.views import APIView
from rest_framework.response import Response

class UserView(APIView):

    def get(self, request, format=None):
        return Response({'detail': "Hello REST World"})