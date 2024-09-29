from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework import status


@api_view(['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def PageNotFound(request):
    return Response({"type": "error", "msg": "404! Page not found"})


@api_view(['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def account_inactive(request):
    return Response({"detail": "Your account is inactive"}, status=status.HTTP_403_FORBIDDEN)
