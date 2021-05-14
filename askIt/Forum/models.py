from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
import datetime


# Create your models here.

# use this model to ID the user

class UserInfo(models.Model):
    phoneNo = models.CharField(max_length=100,unique=True,null=True)
    userType = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.userType


class Questions(models.Model):
    question = models.TextField()
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now=True)
    userWhoAsked = models.ForeignKey(
        User,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    

class Answers(models.Model):
    answer = models.TextField()
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    ansTo = models.ForeignKey(Questions,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer

class Comments(models.Model):
    comment =  models.TextField()
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    commentToAnswer = models.ForeignKey(Answers,on_delete=models.CASCADE) 
    posSentiment=models.BooleanField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

class Replies(models.Model):
    reply = models.TextField()
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    replyToComment = models.ForeignKey(Comments,on_delete=models.CASCADE) 
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

class Skills(models.Model):
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill

