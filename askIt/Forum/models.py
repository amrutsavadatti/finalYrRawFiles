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
    markSheet_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


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
    replyTo = models.TextField(null=True)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
class userResponses(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    qtn = models.ForeignKey(Questions, blank=True, null=True, on_delete=models.CASCADE)
    ans = models.ForeignKey(Answers, blank=True, null=True, on_delete=models.CASCADE)
    cmt = models.ForeignKey(Comments, blank=True, null=True, on_delete=models.CASCADE)
    upVote = models.BooleanField(default=False)
    downVote= models.BooleanField(default=False)

class Skills(models.Model):
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill

class userSkills(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills,on_delete=models.CASCADE)


