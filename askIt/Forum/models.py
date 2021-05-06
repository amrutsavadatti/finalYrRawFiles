from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# ef39d7a9f9ee4c0ca68745eee26cb99a    API_KEY for News_api


# Create your models here.

# use this model to ID the user

class UserCred(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class UserInfo(models.Model):
    fullName = models.CharField(max_length=100)
    userName = models.CharField(max_length=100,unique=True)
    phoneNo = models.CharField(max_length=100,unique=True,null=True)
    userType = models.CharField(max_length=100)
    keyLink = models.OneToOneField(UserCred, on_delete=models.CASCADE)

class Questions(models.Model):
    question = models.TextField()
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    userWhoAsked = models.ForeignKey(UserCred,on_delete=models.CASCADE)

class Answers(models.Model):
    answer = models.TextField()
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    ansTo = models.ForeignKey(Questions,on_delete=models.CASCADE)

class Comments(models.Model):
    comment =  models.TextField()
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    commentToAnswer = models.ForeignKey(Answers,on_delete=models.CASCADE) 

class Replies(models.Model):
    reply = models.TextField()
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    replyToComment = models.ForeignKey(Comments,on_delete=models.CASCADE) 

class Skills(models.Model):
    skill = models.CharField(max_length=100)
    person = models.ManyToManyField(UserCred)
