from django.contrib import admin
from django.urls import path
from Forum import views
from .views import *

urlpatterns = [
    path("", views.display, name = "displayPage"),
    path("login", views.login, name = "Login"),
    path("register1", views.Register1, name = "Register1"),
    path("register2", views.Register2, name = "Register2"),
    path("register3", views.Register3, name = "Register3"),
    path("postAlumni", views.takeToHome, name = "postAlumni"),
    path("postStack", views.home1, name = "postStack"),
    path("profile", views.profile, name = "Profile"),
    path("askAlumni", AjaxHandlerView.as_view()),
    path("alumni", views.alumni, name = "Alumni"),
    path("chat", views.chatBox, name = "chat"),
    path("answers", views.ans, name = "ans"),
    path("abc", views.abc, name = "abc"),
    path("pop", views.populateDb, name = "pop"),
    path("logOut", views.LogOut, name = "LogOut"),
    path("search/", PublisherDocumentView.as_view({'get' : 'list'})),
]