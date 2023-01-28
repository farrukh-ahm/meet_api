from account.models import Profile
from authentication.models import User
from event.models import EventGroup, EventOpinion
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_pic']


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['username', 'name', 'email']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class EventOpinionSerializer(serializers.ModelSerializer):
    
    opioner = serializers.SerializerMethodField(read_only=True)
    opioner_name = serializers.SerializerMethodField(read_only=True)
    event_id = serializers.SerializerMethodField(read_only=True)
    opinioner_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EventOpinion
        fields = [
            'id', 'user', 'event_id',
            'opioner', 'opioner_name', 'opinioner_image',
            'opinion', 'date_created'

            ]

    def get_opioner(self, obj):
        return obj.user.username

    def get_opioner_name(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}"
        return name

    def get_event_id(self, obj):
        return obj.event_post._id

    def get_opinioner_image(self, obj):
        profile = Profile.objects.get(username=obj.user.username)
        serializer  = ProfileSerializer(profile, many=False)
        data = serializer.data
        profile_pic = data['profile_pic']
        return profile_pic

class EventGroupSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    members = serializers.SerializerMethodField(read_only=True)
    opinion_count = serializers.SerializerMethodField(read_only=True)
    members_count = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    opinions = EventOpinionSerializer(many=True, read_only=True)

    class Meta:
        model = EventGroup
        fields = [
            '_id', 'author', 'title', 'description',
            'image', 'details', 'members_count', 'members',
            'opinion_count', 'opinions', 'tags',
            'deadline', 'create_at'
            ]

    def get_author(self, obj):
        serializer = UserSerializer(obj.author, many=False)
        return serializer.data
    
    def get_tags(self, obj):
        space_undo = obj.tags.replace(" ", "")
        tags = list(space_undo.split(","))
        return tags


    def get_members_count(self, obj):
        return obj.members.values().count()

    def get_members(self, obj):
        serializer = UserSerializer(obj.members, many=True)
        return serializer.data

    def get_opinion_count(self, obj):
        return obj.opinion.count()
    

