# from django.shortcuts import render
from authentication.serializers import UserSerializerWithToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


# Create your views here.
@api_view(['GET'])
def intro(request):
    return Response(data={"message": "Hello Event"}, status=status.HTTP_200_OK)