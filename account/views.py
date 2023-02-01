# from django.shortcuts import render
from account.models import Profile
from account.serializer import ProfileSerializer
from authentication.serializers import UserSerializerWithToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

# Create your views here.

User = get_user_model()

@api_view(['GET'])
def intro(request):
    return Response(data={"message": "Hello Account"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = Profile.objects.filter(user=user)
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_username(request, username ,*args, **kwargs):
    user = request.user
    profile = Profile.objects.filter(username=username)
    obj = profile.first()
    serializer = ProfileSerializer(obj, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    data = request.data
    user = request.user
    profile = User.objects.get(id = user.id)
    serializer = UserSerializerWithToken(profile, many=False)
    print(data['first_name'], data['last_name'])
    profile.first_name = data['first_name']
    profile.last_name = data['last_name']
    profile.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_allprofile(request):
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadProfileImage(request):
    data = request.data
    profile = Profile.objects.get(user=request.user)
    profile.profile_pic = request.FILES.get('profile_image')
    profile.save()
    return Response('Profile pic upload')
