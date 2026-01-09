from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """serializer for creating new user accounts"""
# serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    token = serializers.CharField(read_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'password', 'password_confirm',
                  'bio', 'profile_picture', 'token']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match!!'})
        return attrs
        
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user_password = validated_data.pop('password')

        # get_user_model().objects.create_user
        new_user = UserModel.objects.create_user(password=user_password, **validated_data)

        # Generate auth token for the new user
        Token.objects.create(user=new_user)

        return new_user
        
class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login credentials"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

class UserProfileSerializer(serializers.ModelSerializer):
    """serializer for user profile data"""

    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'bio', 'profile_picture'
                  'followers_count', 'following_count']
        read_only_fields = ['id', 'username']

    def get_followers_count(self, obj):
        return obj.get_followers_count()
    
    def get_following_cont(self, obj):
        return obj.get_following_count()