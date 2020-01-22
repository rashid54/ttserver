from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings



class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self,username,email,institution,is_teacher,password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email= self.normalize_email(email)
        user= self.model(username=username,email=email,institution=institution,is_teacher=is_teacher)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,username,email,password):
        """create new super user profile"""
        user= self.create_user(username,email,password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using= self._db)

        return user



class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Model for users table"""
    username = models.CharField(max_length=255, unique=True)
    email= models.EmailField(max_length=255, unique=True)
    institution= models.CharField(max_length=255,blank=True)
    is_teacher= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_email(self):
        """Retrieve email of user"""
        return self.email

    def __str__(self):
        """ Return the string representation of the user as username"""
        return  self.username

class QuestionItem(models.Model):
    """Question item model"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    question = models.CharField(max_length= 255)
    opt1= models.CharField(max_length=255)
    opt2= models.CharField(max_length=255)
    opt3= models.CharField(max_length=255)
    opt4= models.CharField(max_length=255)
    ans= models.CharField(max_length=255)

    def __str__(self):
        """return the only the question"""
        return self.question

class Test(models.Model):
    """Test model"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    testname= models.CharField(max_length=255)
    questions= models.ManyToManyField(QuestionItem)
    duration= models.IntegerField(null=True)
    totalques= models.IntegerField(null=True)

    def __str__(self):
        """return only the testname"""
        return self.testname

class TestResult(models.Model):
    """TestResult model for storing results of tests"""
    test_id= models.ForeignKey(
        'profiles_api.Test',
        on_delete=models.CASCADE
    )
    user_id=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    score= models.IntegerField()

    def __str__(self):
        """return score"""
        return self.score


class SelectedAns(models.Model):
    """SelectedAns model"""
    question_id= models.ForeignKey(
        'profiles_api.QuestionItem',
        on_delete=models.CASCADE
    )
    result_id=models.ForeignKey(
        'profiles_api.TestResult',
        on_delete=models.CASCADE
    )
    selected_answer= models.CharField(max_length=255)

    def __str__(self):
        """return answer only"""
        return self.selected_answer
