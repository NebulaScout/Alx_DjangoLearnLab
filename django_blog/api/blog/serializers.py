from rest_framework import serializers
from django.contrib.auth.models import User

from blog.models import Post

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' ,'username', 'first_name', 'last_name', 'email','password1']
        # read_only_fields = ["id", "date_joined"]

    