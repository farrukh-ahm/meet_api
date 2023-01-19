from authentication.models import User
from event.models import EventGroup
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class EventGroupSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    members = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EventGroup
        fields = '__all__'

    def get_author(self, obj):
        serializer = UserSerializer(obj.author, many=False)
        return serializer.data
    
    def get_members(self, obj):
        serializer = UserSerializer(obj.members, many=True)
        return serializer.data
    