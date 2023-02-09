from account.models import Profile
from event.models import EventGroup
from event.serializers import EventGroupSerializer
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField(read_only=True)
    group_event = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'profile_pic', 'username','email', 'group_event', 'event_count', 'phone_number', 'created', 'updated']
    
    def get_event_count(self, obj):
        """
        Get the number of users joining an event
        """
        event_member = EventGroup.objects.all().filter(members__username=obj.username)
        return event_member.count()
        
    def get_group_event(self, obj):
        event_member = EventGroup.objects.all().filter(members__username=obj.username)
        serializer = EventGroupSerializer(event_member, many=True)
        return serializer.data
    
