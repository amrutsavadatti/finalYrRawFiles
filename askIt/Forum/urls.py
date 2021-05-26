from django.contrib import admin
from django.urls import path
from Forum import views
from .views import *
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path("", views.display, name = "displayPage"),
    #path("login", login_attempt, name = "Login"),
    path("register1", views.Register1, name = "Register1"),
    path("register2", views.Register2, name = "Register2"),
    path('search/', views.autocomplete, name='autocomplete'),
    path("register3", views.runCheck, name = "runCheck"),
    path('token' , token_send , name="token_send"),
    path('verify/<auth_token>' , verify , name="verify"),
    path('accounts/login/' , login_attempt , name="login_attempt"),
    path('accounts' , Account , name="account"),
    path("postAlumni", views.takeToHome, name = "postAlumni"),
    path("postStack", views.home1, name = "postStack"),
    path("profile", views.profile, name = "Profile"),
    # path("askAlumni", login_required(AjaxHandlerView.as_view())),
    path("alumni", views.alumni, name = "Alumni"),
    path("askAlumni", AskAlumni, name = "askAlumni"),
    path("chat", views.chatBox, name = "chat"),
    path("answers/<int:id>", AjaxAnsView.as_view(), name = "ans"),
    path("comments/<int:id>", AjaxComView.as_view(), name = "com"),
    path("profile/<int:id>", views.profileAlumni, name = "ProfileA"),
    # path("notifications", AjaxNotifyView.as_view(), name = "notify"),
    # path("comments/<int:id>", views.save_comment, name = "com"),
    path("postQuestion", views.postQuestion, name = "q"),
    path("searchQuestion", views.searchQuestion, name = "sq"),
    path("abc", views.abc, name = "abc"),
    #path("pop", views.populateDb, name = "pop"),
    path("logOut", views.LogOut, name = "LogOut"),
    path("search/", PublisherDocumentView.as_view({'get' : 'list'})),
    path("searchQ/", QuestionDocumentView.as_view({'get' : 'list'})),
    #path("tatti", tattiFun, name = "poop"),
    path("notifications", notify, name = "notify"),
    path("s", getSkills, name = "gs"),
    path("getIn", getIn, name = "getIn"),
    path("reg2",skillPage,name="skillPage"),

]

# urlpatterns = [
#     path("", views.display, name = "displayPage"),
# ]


