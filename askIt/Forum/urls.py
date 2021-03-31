from django.contrib import admin
from django.urls import path
from Forum import views

urlpatterns = [
    path("", views.display, name = "displayPage"),
    path("login", views.login, name = "Login"),
    path("register1", views.Register1, name = "Register1"),
    path("register2", views.Register2, name = "Register2"),
    path("register3", views.Register3, name = "Register3"),
    path("postAlumni", views.home, name = "postAlumni"),
    path("postStack", views.home1, name = "postStack"),
    path("profile", views.profile, name = "Profile"),
    path("askAlumni", views.askAlumni, name = "AskAlumni"),
]