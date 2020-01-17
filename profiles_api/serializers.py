from rest_framework import serializers
from profiles_api import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','username','email','password')
        extra_kwargs ={
            'password': {
                'write_only': True,
                'style': {'input_type':'password'}
            }
        }

    def create(self,validated_data):
        """Override, create and return a new user"""
        user = models.UserProfile.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            password= validated_data['password']
        )

        return user
