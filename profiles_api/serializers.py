from rest_framework import serializers
from profiles_api import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id','username','email','institution','is_teacher','password')
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
            institution= validated_data['institution'],
            is_teacher= validated_data['is_teacher'],
            password= validated_data['password']
        )

        return user

    def update(self,instance,validated_data):
        """overrides update """
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class QuestionItemSerializer(serializers.ModelSerializer):
    """serializes QuestionItem model"""

    class Meta:
        model = models.QuestionItem
        fields= ('id','user_profile','question','opt1','opt2','opt3','opt4','ans')
        extra_kwargs = {'user_profile':{'read_only':True}}


class TestSerializer(serializers.ModelSerializer):
    """serializes Test """
    class Meta:
        model = models.Test
        fields= ('id','testname','questions','duration','totalques','user_profile')
        extra_kwargs= {'user_profile':{'read_only':True}}


class TestResultSerializer(serializers.ModelSerializer):
    """serializes TestResult"""
    class Meta:
        model= models.TestResult
        fields= ('id','test_id','user_id','score','testname','username')
        extra_kwargs = {'user_id':{'read_only':True}}


class SelectedAnsSerializer(serializers.ModelSerializer):
    """serializes SelectedAns model"""
    class Meta:
        model= models.SelectedAns
        fields= ('id','result_id','question_id','selected_answer')
