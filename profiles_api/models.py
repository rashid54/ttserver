from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager



class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self,username,email,password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email= self.normalize_email(email)
        user= self.model(username=username,email=email)

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
