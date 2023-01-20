from authentication.models import User
from event.models import EventGroup, EventOpinion
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class EventOpinionSerializer(serializers.ModelSerializer):
    
    opioner = serializers.SerializerMethodField(read_only=True)
    opioner_name = serializers.SerializerMethodField(read_only=True)
    event_id = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = EventOpinion
        fields = ['id', 'user', 'event_id' ,'opioner', 'opioner_name', 'opinion']

    def get_opioner(self, obj):
        return obj.user.username
    def get_opioner_name(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}"
        return name
    def get_event_id(self, obj):
        return obj.event_post._id

class EventGroupSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    members = serializers.SerializerMethodField(read_only=True)
    opinion_count = serializers.SerializerMethodField(read_only=True)
    members_count = serializers.SerializerMethodField(read_only=True)
    opinion = EventOpinionSerializer(many=True, read_only=True)

    class Meta:
        model = EventGroup
        fields = ['_id','author','title', 'description' ,'image', 'details', 'members_count', 'members', 'opinion_count', 'opinion', 'tags', 'deadline', 'create_at']

    def get_author(self, obj):
        serializer = UserSerializer(obj.author, many=False)
        return serializer.data
    
    def get_members_count(self, obj):
        return obj.members.values().count()

    def get_members(self, obj):
        serializer = UserSerializer(obj.members, many=True)
        return serializer.data

    def get_opinion_count(self, obj):
        return obj.opinion.count()
    

