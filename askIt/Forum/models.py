from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# ef39d7a9f9ee4c0ca68745eee26cb99a    API_KEY for News_api


# Create your models here.

# use this model to ID the user
class UserCreds(models.Model):
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


# class UserAccount(models.Model):

#     email = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)

    # fullName = models.CharField(max_length=100)
    # userName = models.CharField(max_length=100)
    # phoneNumber = models.CharField(max_length=100)
    # userType = models.CharField(max_length=100)
    # keyLink = models.OneToOneField(UserCreds,on_delete=)

class QuestionsAsked(models.Model):
    Question = models.CharField(max_length=500)
    keyLink = models.ManyToManyField(UserCreds)

class ElasticDemo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()


# For HMi

class AppUser(models.Model):
    fullName = models.CharField(max_length=100)
    userName = models.CharField(max_length=100,unique=True)
    phoneNumber = models.CharField(max_length=100)
    userType = models.CharField(max_length=100)
    keyLink = models.OneToOneField(UserCreds,on_delete = models.CASCADE)




