# from django.shortcuts import render
from datetime import date

from django.contrib.auth import get_user_model
from event.models import EventGroup, EventOpinion
from event.serializers import EventGroupSerializer, EventOpinionSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


# Create your views here.
@api_view(['GET'])
def intro(request):
    return Response(data={"message": "Hello Event"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getAllEvent(request):
    events = EventGroup.objects.all()
    serializer = EventGroupSerializer(events, many=True)
    return Response(data=serializer.data, status = status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authAllEvent(request):
    current_user = request.user
    group_members = EventGroup.objects.all().filter(members__username = current_user.username)
    all_groups = [group._id for group in group_members]
    events = EventGroup.objects.exclude(_id__in=all_groups)
    serializer = EventGroupSerializer(events, many=True)
    return Response(data=serializer.data, status = status.HTTP_200_OK)


@api_view(['GET'])
def getEvent(request, event_id):
    qs = EventGroup.objects.filter(_id = event_id)
    if not qs.exists():
        return Response({"message": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)
    event = qs.first()
    serializer = EventGroupSerializer(event, many=False)
    return Response(data=serializer.data, status = status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myEvent(request):
    current_user = request.user
    group_members = EventGroup.objects.all().filter(members__username = current_user.username)
    serializer = EventGroupSerializer(group_members, many=True)
    return Response(data=serializer.data, status = status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authorEvent(request):
    current_user = request.user
    author = EventGroup.objects.all().filter(author=current_user)
    serializer = EventGroupSerializer(author, many=True)
    return Response(data=serializer.data, status = status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createEvent(request):
    user = request.user
    data = request.data
    file = request.FILES.get('event_file')
    eventCreate = EventGroup.objects.create(
        author = user,
        title = data['title'],
        image= file,
        description = data['description'],
        details = data['details'],
        deadline = data['deadline'],
        tags = data['tags']
    )
    eventCreate.members.add(user)
    serializer = EventGroupSerializer(eventCreate)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadEventFile(request):
    data = request.data
    event_id = data['event_id']
    event = EventGroup.objects.get(_id=event_id)
    event.image = request.FILES.get('event_file')
    event.save()
    return Response('Event Photo upload Done')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteEvent(request, event_id):
    user = request.user
    qs = EventGroup.objects.filter(_id = event_id)
    if not qs.exists():
        return Response({"message": "Event does not exit"}, status=status.HTTP_404_NOT_FOUND)
    event = qs.first()
    if (user == event.author or user.is_superuser == True):
        event.delete()
        return Response({"message": "Event Removed Successfully"}, status=status.HTTP_200_OK)
    return Response({"message": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateEvent(request, event_id):
    user = request.user
    data = request.data
    qs = EventGroup.objects.filter(_id = event_id, author=user)
    event = qs.first()
    if not qs.exists():
        return Response({"message": "Event does not exit or You are not authorized"}, status=status.HTTP_404_NOT_FOUND)
    event.title = data['title'],
    event.description = data['description'],
    event.details = data['details'],
    event.deadline = data['deadline']
    event.tags = data['tags']
    event.save()
    serializer = EventGroupSerializer(event, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def actionEvent(request, event_id):
    user = request.user
    qs = EventGroup.objects.filter(_id=event_id)
    if not qs.exists():
        return Response({"message": "Event Does Not Exist Or You are not authorized"}, status=status.HTTP_400_BAD_REQUEST)
    event = qs.first()
    if user == event.author:
        event.delete()
        return Response({"message": "Event Deleted"}, status=status.HTTP_200_OK)

    today = date.today()
    deadline = event.deadline
    if today <= deadline:
        members = [member['username'] for member in event.members.values()]
        if user.username not in members:
            event.members.add(user)
            return Response({"message": "You Joined the Meet!"}, status=status.HTTP_200_OK)
        else:
            event.members.remove(user)
            return Response({"message": "You left the Meet"}, status=status.HTTP_200_OK)
    return Response({"message": "TimeOut"}, status=status.HTTP_204_NO_CONTENT)



# Event Opinion 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_opinion_create(request, event_id):
    qs = EventGroup.objects.filter(_id= event_id)
    if not qs.exists():
        return Response({"message": "Event Not Found"}, status=status.HTTP_404_NOT_FOUND)
    obj = qs.first()
    user = request.user
    data = request.data
    opinion_add = EventOpinion.objects.create(
        user = user,
        event_post = obj,
        opinion = data['opinion']
    )
    obj.opinion.add(opinion_add)
    serializer = EventOpinionSerializer(opinion_add, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['Delete'])
@permission_classes([IsAuthenticated])
def event_opinion_delete(request, event_id, opinion_id):
    qs = EventGroup.objects.filter(_id= event_id)
    if not qs.exists():
        return Response({"message": "Event Not Found"}, status=status.HTTP_404_NOT_FOUND)
    obj = qs.first()
    user = request.user
    data = request.data
    opinion_qs = EventOpinion.objects.filter(id = opinion_id)
    if not opinion_qs.exists():
        return Response({"message": "Opinion Not Found"}, status=status.HTTP_404_NOT_FOUND)
    opinion = opinion_qs.first()
    if (user == opinion.user or user.is_superuser == True or user == obj.author):
        remove_opinion = obj.opinion.remove(opinion)
        opinion.delete()
        return Response({"message": "Opinion Deleted Successfully"}, status=status.HTTP_200_OK)
    return Response({"message": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def event_opinion_update(request, event_id, opinion_id):
    qs = EventGroup.objects.filter(_id= event_id)
    if not qs.exists():
        return Response({"message": "Event Not Found"}, status=status.HTTP_404_NOT_FOUND)
    obj = qs.first()
    user = request.user
    data = request.data
    opinion_qs = EventOpinion.objects.filter(id = opinion_id, user = user)
    if not opinion_qs.exists():
        return Response({"message": "Opinion Not Found"}, status=status.HTTP_404_NOT_FOUND)
    opinion = opinion_qs.first()
    opinion.opinion = data['opinion']
    opinion.save()
    serializer = EventOpinionSerializer(opinion, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


