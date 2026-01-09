from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Extended user model for social media platforms"""

    bio = models.TextField(max_length=500, blank=True, help_text="Short biography about the user")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, help_text="User's profile image")
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True, help_text="Users who follow this user")

    def __str__(self):
        return self.username
    
    def get_followers_count(self):
        return self.followers.count()
    
    # def get_following_count(self):
    #     return self.following.count()