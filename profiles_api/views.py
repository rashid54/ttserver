from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

class UserProfileViewSet(viewsets.ModelViewSet):
    """Viewset for handling profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    # authentication_classes= (TokenAuthentication,)
    # permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class QuestionItemViewSet(viewsets.ModelViewSet):
    """Handles question items"""
    serializer_class = serializers.QuestionItemSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = models.QuestionItem.objects.all()
    filter_backends= (filters.SearchFilter,)
    search_fields = ('question','id',)

    def perform_create(self,serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

class TestViewSet(viewsets.ModelViewSet):
    """Handles Test """
    serializer_class= serializers.TestSerializer
    queryset= models.Test.objects.all()
    authentication_classes= (TokenAuthentication,)
    filter_backends= (filters.SearchFilter,)
    search_fields= ('testname','id',)


    def perform_create(self,serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)



class GetUser(viewsets.ViewSet):
    """Viewset for finding user id"""
    authentication_classes= (TokenAuthentication,)
    def list(self, request):
        return Response(
            {
                "id":request.user.id,
                "username":request.user.username,
                "email":request.user.email,
                "institution":request.user.institution,
            }
        )

class GetTestQuestion(viewsets.ViewSet):
    """For getting the questions of any test"""

    def list(self,request,pk):
        sql="SELECT * FROM profiles_api_questionitem INNER JOIN (profiles_api_test INNER JOIN profiles_api_test_questions ON profiles_api_test.id = profiles_api_test_questions.test_id) ON profiles_api_questionitem.id =profiles_api_test_questions.questionitem_id where profiles_api_test.id = "+ pk + " ;"
        queryset= models.QuestionItem.objects.raw(sql)
        serializer= serializers.QuestionItemSerializer(queryset,many=True)
        return Response(serializer.data)

class TestResultViewSet(viewsets.ModelViewSet):
    """Handles TestResult model"""
    serializer_class=serializers.TestResultSerializer
    queryset= models.TestResult.objects.all()
    authentication_classes=(TokenAuthentication,)
    filter_backends= (filters.SearchFilter,)
    search_fields= ('test_id',)

    def perform_create(self,serializer):
        """Sets the user_id to the logged in user"""
        serializer.save(user_id=self.request.user)

class SelectedAnsViewSet(viewsets.ModelViewSet):
    """Handles SelectedAns model"""
    serializer_class= serializers.SelectedAnsSerializer
    queryset= models.SelectedAns.objects.all()
    authentication_classes=(TokenAuthentication,)
    filter_backends= (filters.SearchFilter,)
    search_fields= ('result_id',)
