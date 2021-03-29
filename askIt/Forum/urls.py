from django.contrib import admin
from django.urls import path
from Forum import views

urlpatterns = [
    path("", views.display, name = "displayPage"),
    path("login", views.login, name = "Login"),
    path("register", views.Register, name = "Register"),
    path("postAlumni", views.home, name = "postAlumni"),
    path("postStack", views.home1, name = "postStack"),
    path("profile", views.profile, name = "Profile"),
    path("askAlumni", views.profile, name = "AskAlumni"),
]