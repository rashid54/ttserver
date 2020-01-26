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

from rest_framework.authtoken.models import Token

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions
from profiles_api.token_generator import account_activation_token,generateSecureRandomString

class UserProfileViewSet(viewsets.ModelViewSet):
    """Viewset for handling profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    # authentication_classes= (TokenAuthentication,)
    # permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def perform_create(self,serializer):
        """sends confirmation email"""
        instance=serializer.save()
        current_site=get_current_site(self.request)
        email_subject='Activate Your Account'
        message=render_to_string('activate_account.html',{
            'user':instance,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(instance.id)),
            'token':account_activation_token.make_token(instance),
        })
        to_email= instance.email
        email= EmailMessage(email_subject,message,to=[to_email])
        email.send()


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self,request,*args,**kwargs):
        try:
            user=models.UserProfile.objects.get(username=request.data['username'])
            if user.is_active is not True:
                return Response({'is_active':user.is_active})
        except(TypeError, ValueError, OverflowError, models.UserProfile.DoesNotExist):
            user = None
        response=super(UserLoginApiView,self).post(request,*args,**kwargs)
        token= Token.objects.get(key=response.data['token'])
        return Response({'token':token.key,'id':token.user_id,'is_active':user.is_active})


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
                "is_teacher":request.user.is_teacher,
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
    search_fields= ('test_id__testname',)

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



def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = models.UserProfile.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, models.UserProfile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('{Your Email has been confirmed and your Account has been Activated !}')
    else:
        return HttpResponse('{The Activation link is invalid !}')

def send_confirm_email(request,uid):
    """sends email for confirmation"""
    user=models.UserProfile.objects.get(id=uid)
    current_site=get_current_site(request)
    email_subject='Activate Your Account'
    message=render_to_string('activate_account.html',{
        'user':user,
        'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(uid)),
        'token':account_activation_token.make_token(user),
    })
    to_email= user.email
    email= EmailMessage(email_subject,message,to=[to_email])
    email.send()
    return JsonResponse(
        {
            "status":"The confirmation email has been sent.",
        }
    )

## todo fix forgot password option
@csrf_exempt
def reset_password_email(request):
    """ Sends reset password email"""
    if request.method == 'POST' :
        try:
            print(request.POST)
            user = models.UserProfile.objects.get(email=request.POST.get('email',''))
            current_site=get_current_site(request)
            email_subject='Password Reset'
            message=render_to_string('reset_password.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':account_activation_token.make_token(user),
            })
            to_email= user.email
            email= EmailMessage(email_subject,message,to=[to_email])
            email.send()
            return JsonResponse(
                {
                    "status":"The Reset password email has been sent."
                }
            )
        except(TypeError, ValueError, OverflowError, models.UserProfile.DoesNotExist):
            user = None
            return JsonResponse(
                {
                    "status":"No matching account found"
                }
            )
    else :
        return JsonResponse(
            {
                "status":"only post method is available"
            }
        )

def reset_password(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = models.UserProfile.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, models.UserProfile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        newpassword = generateSecureRandomString(8)
        user.set_password(newpassword)
        user.save()
        return HttpResponse('{Your password has been successfully reset. Your new password is : '+newpassword+' }')
    else:
        return HttpResponse('{Password reset failed. The Reset link is invalid !}')

class ResetPassword(viewsets.ViewSet):
    """for resetting password"""

    def create(self,request):
        """ Sends reset password email"""
        try:
            print(request.data)
            user = models.UserProfile.objects.get(email=request.data['email'])
            current_site=get_current_site(request)
            email_subject='Reset Password'
            message=render_to_string('reset_password.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':account_activation_token.make_token(user),
            })
            to_email= user.email
            email= EmailMessage(email_subject,message,to=[to_email])
            email.send()
            return Response(
                {
                    "status":"The Reset password email has been sent."
                }
            )
        except(TypeError, ValueError, KeyError, OverflowError, models.UserProfile.DoesNotExist):
            user = None
            return Response(
                {
                    "status":"No matching account found."
                }
            )

    # def list(self,request, uidb64, token):
    #     """for resetting the password"""
    #     try:
    #         uid = force_bytes(urlsafe_base64_decode(uidb64))
    #         user = models.UserProfile.objects.get(id=uid)
    #     except(TypeError, ValueError, OverflowError, models.UserProfile.DoesNotExist):
    #         user = None
    #     if user is not None and account_activation_token.check_token(user, token):
    #         newpassword = generateSecureRandomString(8)
    #         user.set_password(newpassword)
    #         user.save()
    #         return HttpResponse('{Your password has been successfully reset. Your new password is : '+newpassword+' }')
    #     else:
    #         return HttpResponse('{Password reset failed. The Reset link is invalid !}')
