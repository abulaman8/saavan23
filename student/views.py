from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@api_view(['GET'])
def home(request):
    content = {'message': 'Hello, World!'}
    return Response(content, status=status.HTTP_200_OK)



