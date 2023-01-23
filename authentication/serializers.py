from authentication.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreationSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=40)
    email=serializers.EmailField(max_length=80)
    phone_number=PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'phone_number', 'password', 'isAdmin']
    
    def get_isAdmin(self, obj):
        return obj.is_staff

    def validate(self, attrs):

        
        email_exists = User.objects.filter(username=attrs['email']).exists()

        if email_exists:
            raise serializers.ValidationError(detail="User with email exists")

        
        phonenumber_exists = User.objects.filter(username=attrs['phone_number']).exists()

        if phonenumber_exists:
            raise serializers.ValidationError(detail="User with phone number exists")

        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email = validated_data['email'],
            username = validated_data['email'].split('@')[0],
            phone_number = validated_data['phone_number'],
            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializerWithToken(UserCreationSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username','email', 'phone_number', 'password', 'isAdmin', 'token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    def get_username(self, obj):
        return obj.username